from .base import *  # noqa
from .base import env

DEBUG = True

SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    default='!!!SET DJANGO_SECRET_KEY!!!',
)
ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '',
    }
}

EMAIL_BACKEND = env(
    'DJANGO_EMAIL_BACKEND', 
    default='django.core.mail.backends.console.EmailBackend'
)

INSTALLED_APPS += ['debug_toolbar']  # noqa F405
INSTALLED_APPS += ["django_extensions"]  # noqa F405

# django-debug-toolbar
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa F405
DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': ['debug_toolbar.panels.redirects.RedirectsPanel'],
    'SHOW_TEMPLATE_CONTEXT': True,
}
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
