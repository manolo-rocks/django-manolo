import os
import logging
from .base import *  # noqa
from .base import env

log = logging.getLogger(__name__)

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

MEDIA_ROOT = "/data/media/"
STATIC_ROOT = "/data/static/"

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [
    '.manolo.rocks',  # Allow domain and subdomains
    '.manolo.rocks.',  # Also allow FQDN and subdomains
    'localhost',
]

DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405


INTERNAL_IPS = ["127.0.0.1", "10.0.2.2", "181.66.194.247"]


# Create a function to determine if debug toolbar should be shown
def show_toolbar(request):
    # Always show to superusers
    if hasattr(request, '_asgi_base_scope'):
        client_addr = request.META.get('REMOTE_ADDR', None)
        log.info(f"XXXXXX Client address: {client_addr}")
        print(f"XXXXXX Client address: {client_addr}")
        return client_addr in INTERNAL_IPS

    # Show to internal IPs    try:
    try:
        if hasattr(request, 'user') and request.user.is_authenticated and request.user.is_superuser:
            return True
    except Exception:
        return False


# Add debug toolbar middleware
if 'django_debug_toolbar' not in INSTALLED_APPS:
    INSTALLED_APPS += ['debug_toolbar']

if 'debug_toolbar.middleware.DebugToolbarMiddleware' not in MIDDLEWARE:
    # Insert as early as possible, but after any other middleware that encodes the response's content
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# Override default toolbar configuration
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'manolo.settings.production.show_toolbar',
    # Adjust with your actual module path
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': False,
    'ENABLE_STACKTRACES': True,
}

# Configure debug toolbar panels
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]
