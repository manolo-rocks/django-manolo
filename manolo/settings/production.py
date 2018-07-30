import os
import json

from django.core.exceptions import ImproperlyConfigured

from .base import *

STATIC_ROOT = "/var/www/manolo/static/"
MEDIA_ROOT = "/var/www/manolo/media/"

DEBUG = False

ALLOWED_HOSTS = [
    '.manolo.rocks',  # Allow domain and subdomains
    '.manolo.rocks.',  # Also allow FQDN and subdomains
]

with open(SECRETS_FILE) as f:
    secrets = json.loads(f.read())

SECRET_KEY = get_secret('SECRET_KEY')

PREMIUM_INSTITUTIONS = [
    "minjus",
    "minam",
    "mincetur",
    "mtc",
    "ingemmet",
    "perucompras",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PASS'),
        'HOST': get_secret('DB_HOST'),
        'PORT': get_secret('DB_PORT'),
    }
}
