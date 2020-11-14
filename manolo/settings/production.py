from .base import *  # noqa
from .base import env


STATIC_ROOT = "/var/www/manolo/static/"
MEDIA_ROOT = "/var/www/manolo/media/"

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [
    '.manolo.rocks',  # Allow domain and subdomains
    '.manolo.rocks.',  # Also allow FQDN and subdomains
]

DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405
