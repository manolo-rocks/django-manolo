import os
import json

from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('AniversarioPeru', 'aniversarioperu1@gmail.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = [
    '.manolo.rocks',  # Allow domain and subdomains
    '.manolo.rocks.',  # Also allow FQDN and subdomains
]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRETS_FILE = os.path.join(BASE_DIR, '..', 'config.json')

with open(SECRETS_FILE) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret('SECRET_KEY')

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
