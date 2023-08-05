from __future__ import print_function
import time
import re
import socket
from datetime import datetime

import feedparser

from six.moves import http_client as http
from six import text_type
from six.moves.urllib.request import Request, urlopen

from django.utils.timezone import utc

from feedz import conf
from feedz import models
from feedz import feedutil
from feedz import exceptions
from feedz.utils import get_default_logger, truncate_field_data
from feedz.backends import backend_or_default

class FeedImporter(object):
    """Import/Update feeds.

    :keyword post_limit: See :attr`post_limit`.
    :keyword update_on_import: See :attr:`update_on_import`.
    :keyword logger: See :attr:`logger`.
    :keyword include_categories: See :attr:`include_categories`.
    :keyword include_enclosures: See :attr:`include_enclosures`.
    :keyword timeout: See :attr:`timeout`.

    .. attribute:: post_limit

        Default number of posts limit.

    .. attribute:: update_on_import

        By default, fetch new posts when a feed is imported

    .. attribute:: logger

       The :class:`logging.Logger` instance used for logging messages.

    .. attribute:: include_categories

        By default, include feed/post categories.

    .. attribute:: include_enclosures

        By default, include post enclosures.

    .. attribute:: timeout

        Default feed timeout.

    .. attribute:: parser

        The feed parser used. (Default: :mod:`feedparser`.)

    """
    parser = feedparser
    post_limit = conf.DEFAULT_POST_LIMIT
    include_categories = conf.STORE_CATEGORIES
    include_enclosures = conf.STORE_ENCLOSURES
    update_on_import = True
    post_model = models.Post
    feed_model = models.Feed
    category_model = models.Category
    enclosure_model = models.Enclosure
    post_field_handlers = {
        "content": feedutil.find_post_content,
        "date_published": feedutil.date_to_datetime("published_parsed"),
        #"date_updated": feedutil.date_to_datetime("updated_parsed"),
        "date_updated": feedutil.date_to_datetime("published_parsed"),
        "link": lambda feed_obj, entry: entry.get("link") or feed_obj.feed_url,
        "feed": lambda feed_obj, entry: feed_obj,
        "guid": feedutil.get_entry_guid,
        "title": lambda feed_obj, entry: entry.get("title",
                                                    "(no title)").strip(),
        "author": lambda feed_obj, entry: entry.get("author", "").strip(),
    }

    def __init__(self, **kwargs):
        self.post_limit = kwargs.get("post_limit", self.post_limit)
        self.update_on_import = kwargs.get("update_on_import",
                                            self.update_on_import)
        self.logger = kwargs.get("logger", get_default_logger())
        self.include_categories = kwargs.get("include_categories",
                                        self.include_categories)
        self.include_enclosures = kwargs.get("include_enclosures",
                                        self.include_enclosures)
        self.timeout = kwargs.get("timeout", conf.FEED_TIMEOUT)
        self.backend = backend_or_default(kwargs.get("backend"))
        self.post_model = self.backend.get_post_model()

    def parse_feed(self, feed_url, etag=None, modified=None, timeout=None,
            maxlen=None):
        """Parse feed using the current feed parser.

        :param feed_url: URL to the feed to parse.

        :keyword etag: E-tag recevied from last parse (if any).
        :keyword modified: ``Last-Modified`` HTTP header received from last
            parse (if any).
        :keyword timeout: Parser timeout in seconds.

        """
        prev_timeout = socket.getdefaulttimeout()
        timeout = timeout or self.timeout

        socket.setdefaulttimeout(timeout)
        try:
            if maxlen:
                headers = self.early_headers(feed_url)
                contentlen = int(headers.get("content-length") or 0)
                if contentlen > maxlen:
                    raise exceptions.FeedCriticalError(
                        text_type(models.FEED_GENERIC_ERROR_TEXT))

            feed = self.parser.parse(feed_url,
                                     etag=etag,
                                     modified=modified)
        finally:
            socket.setdefaulttimeout(prev_timeout)

        return feed

    def early_headers(self, feed_url):

        class HeadRequest(Request):

            def get_method(self):
                return "HEAD"

        return urlopen(HeadRequest(feed_url)).headers

    def real_headers(self, feed_url):
        return urlopen(Request(feed_url))

    def import_feed(self, feed_url, force=None, local=False):
        """Import feed.

        If feed is not seen before it will be created, otherwise
        just updated.

        :param feed_url: URL to the feed to import.
        :keyword force: Force import of feed even if it's been updated
            recently.
        """
        feed_url = feed_url.strip()
        feed = None
        try:
            feed_obj = self.feed_model.objects.get(feed_url=feed_url)
        except self.feed_model.DoesNotExist:
            try:
                feed = self.parse_feed(feed_url)
            except socket.timeout:
                self.feed_model.objects.create(feed_url=feed_url, sort=0)
                raise exceptions.TimeoutError(
                        text_type(models.FEED_TIMEDOUT_ERROR_TEXT))
            except Exception:
                feed = {"status": 500}

            default_status = http.OK if local else http.NOT_FOUND

            status = feed.get("status", default_status)
            if status == http.NOT_FOUND:
                raise exceptions.FeedNotFoundError(
                        text_type(models.FEED_NOT_FOUND_ERROR_TEXT))
            if status not in models.ACCEPTED_STATUSES:
                raise exceptions.FeedCriticalError(
                        text_type(models.FEED_GENERIC_ERROR_TEXT),
                        status=status)

            # Feed can be local/fetched with a HTTP client.
            status = feed.get("status") or feed.get("status\n") or http.OK

            if status == http.FOUND or status == http.MOVED_PERMANENTLY:
                if feed_url != feed.href:
                    return self.import_feed(feed.href, force=force)

            feed_name = feed.channel.get("title", "(no title)").strip()
            feed_data = truncate_field_data(self.feed_model, {
                            "sort": 0,
                            "name": feed_name,
                            "description": feed.channel.get("description", ""),
            })
            feed_obj = self.feed_model.objects.update_or_create(
                                            feed_url=feed_url, **feed_data)

        if self.include_categories:
            feed_obj.categories.add(*self.get_categories(feed.channel))

        if self.update_on_import:
            feed_obj = self.update_feed(feed_obj, feed=feed, force=force)

        return feed_obj

    def get_categories(self, obj):
        """Get and save categories."""
        return [self.create_category(*cat)
                    for cat in getattr(obj, "categories", [])]

    def create_category(self, domain, name):
        """Create new category.

        :param domain: The category domain.
        :param name: The name of the category.

        """
        return self.category_model.objects.update_or_create(
                      name=name.strip(),
                      domain=domain and domain.strip() or "")

    def update_feed(self, feed_obj, feed=None, force=False):
        """Update (refresh) feed.

        The feed must already exist in the system, if not you have
        to import it using :meth:`import_feed`.

        :param feed_obj: the Feed object
        :keyword feed: If feed has already been parsed you can pass the
            structure returned by the parser so it doesn't have to be parsed
            twice.
        :keyword force: Force refresh of the feed even if it has been
            recently refreshed already.

        """

        now = datetime.utcnow().replace(tzinfo=utc)
        already_fresh = (feed_obj.date_last_refresh and
                         now < feed_obj.date_last_refresh +
                         conf.MIN_REFRESH_INTERVAL)

        if already_fresh and not force:
            self.logger.info(
                    "Feed %s is fresh. Skipping refresh." % feed_obj.feed_url)
            return feed_obj

        limit = self.post_limit
        if not feed:
            last_modified = None
            if feed_obj.http_last_modified and not force:
                last_modified = feed_obj.http_last_modified.timetuple()
            etag = feed_obj.http_etag if not force else None

            try:
                feed = self.parse_feed(feed_obj.feed_url,
                                       etag=etag,
                                       modified=last_modified)
            except socket.timeout:
                return feed_obj.save_timeout_error()
            except Exception:
                return feed_obj.save_generic_error()

        # Feed can be local/ not fetched with HTTP client.
        status = feed.get("status", http.OK)
        if status == http.NOT_MODIFIED and not force:
            return feed_obj

        if feed_obj.is_error_status(status):
            return feed_obj.set_error_status(status)

        if feed.entries:
            sorted_by_date = feedutil.entries_by_date(feed.entries, limit)
            for entry in sorted_by_date:
                self.import_entry(entry, feed_obj)

        feed_obj.date_last_refresh = now
        feed_obj.http_etag = feed.get("etag", "")
        if hasattr(feed, "modified") and feed.modified:
            try:
                as_ts = time.mktime(feed.modified)
                feed_obj.http_last_modified = datetime.fromtimestamp(
                        as_ts).replace(tzinfo=utc)
            except TypeError:
                pass

        self.logger.debug("uf: %s Saving feed object..." % (
                            feed_obj.feed_url))

        feed_obj.save()
        return feed_obj

    def create_enclosure(self, **kwargs):
        """Create new enclosure."""
        kwargs.setdefault("length", 0)
        return self.enclosure_model.objects.update_or_create(**kwargs)

    def get_enclosures(self, entry):
        """Get and create enclosures for feed."""
        return [self.create_enclosure(url=enclosure.href,
                                    length=enclosure.length,
                                    type=enclosure.type)
                    for enclosure in getattr(entry, "enclosures", [])
                        if enclosure and hasattr(enclosure, "length")]

    def post_fields_parsed(self, entry, feed_obj):
        """Parse post fields."""
        return dict((key, handler(feed_obj, entry))
                        for key, handler in self.post_field_handlers.items())

    def import_entry(self, entry, feed_obj):
        """
        Import feed post entry.

        Note, feed_obj.feed_url can be either a URL or full RSS document.
        """
        from feedz.models import BlacklistedDomain
        print('='*80)
        is_document = False
        if not feed_obj.feed_url.endswith('.rss') and not feed_obj.feed_url.endswith('.html') and not feed_obj.feed_url.endswith('.xml'):
            is_document = True
#             print('Ignoring corrupt feed URL of length %i.' % len(feed_obj.feed_url))
#             print('feed_obj.feed_url:', feed_obj.feed_url)
#             print(type(feed_obj), feed_obj)
#             raise
#             return
            self.logger.debug("Importing document %s..." % feed_obj.id)
        else:
            self.logger.debug("Importing entry %s..." % feed_obj.feed_url)

        fields = self.post_fields_parsed(entry, feed_obj)

        # Extract link from summary instead of link field if pattern specified.
        if feed_obj.summary_detail_link_regex:
            if 'summary_detail' in entry:
                # Old Reddit RSS format.
                link_matches = re.findall(
                    feed_obj.summary_detail_link_regex,
                    entry['summary_detail']['value'],
                    re.I|re.DOTALL)
                self.logger.debug('Summary detail links: '+str(link_matches))
                if link_matches:
                    fields['link'] = link_matches[0].strip()
            elif 'summary' in entry:
                # New Reddit RSS format.
                link_matches = re.findall(
                    feed_obj.summary_detail_link_regex,
                    entry['summary'],
                    re.I|re.DOTALL)
                self.logger.debug('Summary detail links v2: '+str(link_matches))
                if link_matches:
                    fields['link'] = link_matches[0].strip()

        if conf.LINK_URL_REGEXES:
            for pattern in conf.LINK_URL_REGEXES:
                _matches = pattern.findall(fields['link'])
                if _matches:
                    fields['link'] = _matches[0]

        # Check to see if domain has been blacklisted.
        if BlacklistedDomain.is_blacklisted(fields['link']):
            self.logger.info("Ignoring blacklisted URL: %s" % (fields['link']))
            return

        post = self.post_model.objects.update_or_create(feed_obj, **fields)
        if not post:
            self.logger.debug("Unable to update or create post from entry: %s" % (
                entry))
            return

        if not post.article_content and conf.GET_ARTICLE_CONTENT:
            self.logger.debug('Download article content from %s...' % post.link)
            try:
                post.retrieve_article_content()
            except Exception as e:
                self.logger.error('Error: Unable to retrieve %s: %s' % (post.link, e))

        if self.include_enclosures:
            post.enclosures.add(*(self.get_enclosures(entry) or []))
        if self.include_categories:
            post.categories.add(*(self.get_categories(entry) or []))

        if is_document:
            self.logger.debug("ie: %s Post successfully imported..." % feed_obj.id)
        else:
            self.logger.debug("ie: %s Post successfully imported..." % feed_obj.feed_url)

        return post
