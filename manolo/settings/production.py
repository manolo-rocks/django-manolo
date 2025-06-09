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
    'stag.manolo.rocks',  # Staging environment
    'localhost',
]

DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405


# Axes configuration
AXES_FAILURE_LIMIT = 5  # Block after 5 failed attempts
AXES_COOLOFF_TIME = 1   # Block for 1 hour
AXES_LOCKOUT_PARAMETERS = ['ip_address', 'username']
AXES_ENABLE_ADMIN = True  # See blocked IPs in admin
