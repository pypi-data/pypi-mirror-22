# Django settings for testproj project.

import os
import sys
# import source code dir
sys.path.insert(0, os.path.join(os.getcwd(), os.pardir))

SITE_ID = 69932

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = "mysecretkeytest"
USE_TZ = True

ROOT_URLCONF = "tests.urls"

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

#TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

COVERAGE_EXCLUDE_MODULES = ("feedz",
                            "feedz.admin",
                            "feedz.maintenance",
                            "feedz.management*",
                            "feedz.tests*",
                            "feedz.models",
                            "feedz.managers",
                            "feedz.utils",
)

here = os.path.abspath(os.path.dirname(__file__))

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_VHOST = "/"
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"

CELERY_DEFAULT_EXCHANGE = "testdjangofeeds"
CELERY_DEFAULT_QUEUE = "testdjangofeeds"
CELERY_QUEUES = {
    "testdjangofeeds": {
        "binding_key": "testdjangofeeds",
    }
}
CELERY_DEFAULT_ROUTING_KEY = "testdjangofeeds"

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb.sqlite',
    }
}

USE_TZ = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django_nose',
    #'djcelery',
    'feedz',
    'pytz',
)


SEND_CELERY_TASK_ERROR_EMAILS = False

if os.environ.get("TEST_REDIS_POSTS"):
    DJANGOFEEDS_POST_STORAGE_BACKEND = "redis"
