Django-Feedz
============

[![](https://img.shields.io/pypi/v/django-feedz.svg)](https://pypi.python.org/pypi/django-feedz) [![Build Status](https://img.shields.io/travis/chrisspen/django-feedz.svg?branch=master)](https://travis-ci.org/chrisspen/django-feedz) [![](https://pyup.io/repos/github/chrisspen/django-feedz/shield.svg)](https://pyup.io/repos/github/chrisspen/django-feedz)

A Django model for storing and analyzing RSS/Atom feeds.

Development
-----------

To run unittests across multiple Python versions, install:

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python-dev python3-dev python3.3-minimal python3.3-dev python3.4-minimal python3.4-dev python3.5-minimal python3.5-dev python3.6 python3.6-dev

To run all [tests](http://tox.readthedocs.org/en/latest/):

    export TESTNAME=; tox

To run tests for a specific environment (e.g. Python 2.7 with Django 1.8):
    
    export TESTNAME=; tox -e py27-django18

To run a specific test:
    
    export TESTNAME=.test_importers.TestFeedImporter.test_entry_limit; tox -e py27-django18

To run the [documentation server](http://www.mkdocs.org/#getting-started) locally:

    mkdocs serve -a :9999

To [deploy documentation](http://www.mkdocs.org/user-guide/deploying-your-docs/), run:

    mkdocs gh-deploy --clean

To build and deploy a versioned package to PyPI, verify [all unittests are passing](https://travis-ci.org/chrisspen/django-feedz), and then run:

    python setup.py sdist
    python setup.py sdist upload
