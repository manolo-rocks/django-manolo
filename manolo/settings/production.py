from .base import *

DEBUG = False

ADMINS = (
    ('Carlos', 'carlos@manolo.rocks'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = [
    '.manolo.rocks',  # Allow domain and subdomains
    '.manolo.rocks.',  # Also allow FQDN and subdomains
]

SECRET_KEY = get_secret('SECRET_KEY')
PREMIUM_INSTITUTIONS = get_secret('premium_institutions')
