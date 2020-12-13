import os
from .base import *  # noqa
from .base import env

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

MEDIA_ROOT = "/data/media/"
STATIC_ROOT = "/data/static/"

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [
    '.manolo.rocks',  # Allow domain and subdomains
    '.manolo.rocks.',  # Also allow FQDN and subdomains
]

DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405

TWITTER_CONSUMER_KEY = env("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = env("TWITTER_CONSUMER_SECRET")
TWITTER_OAUTH_TOKEN = env("TWITTER_OAUTH_TOKEN")
TWITTER_OAUTH_TOKEN_SECRET = env("TWITTER_OAUTH_TOKEN_SECRET")
