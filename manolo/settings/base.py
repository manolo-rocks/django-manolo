import json
import sys
import os
from os.path import join, abspath, dirname

from django.core.exceptions import ImproperlyConfigured

# PATH vars
DEBUG = True

ADMINS = (
    ('AniversarioPeru', 'aniversarioperu1@gmail.com'),
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = BASE_DIR + '/../run/devdata/media/'
LOG_DIR = BASE_DIR + "/../run/devdata/logs/"
STATIC_ROOT = BASE_DIR + '/../run/devdata/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '..', 'media'),
    os.path.join(BASE_DIR, '..', 'manolo/assets'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'CHANGE THIS!!!'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['manolo/templates'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # needed for building sitemaps
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'debug': True,
        },
    }
]

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'manolo.urls'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'manolo.wsgi.application'

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'bootstrap4',
    'bootstrap_themes',
    'crispy_forms',
    'registration',
    'rest_framework',
    'rest_framework_swagger',
)

PROJECT_APPS = (
    'visitors',
    'api',
    'cazador',
)

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS

SIMPLE_LOG_FORMAT = '%(levelname)s %(message)s'
VERBOSE_LOG_FORMAT = '[%(asctime)s] [%(levelname)s] [%(threadName)s] ' \
                     '[%(name)s] [%(lineno)d] %(message)s'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': VERBOSE_LOG_FORMAT
        },
        'simple': {
            'format': SIMPLE_LOG_FORMAT
        },
    },

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'terminal': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + 'manolo.rocks.main.log',
            'formatter': 'verbose',
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + 'manolo.rocks.main.debug.log',
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['terminal', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'visitors': {
            'handlers': ['terminal', 'file', 'mail_admins'],
            'level': 'DEBUG',
        },
        'api': {
            'handlers': ['terminal', 'file', 'mail_admins'],
            'level': 'DEBUG',
        },
        'cazador': {
            'handlers': ['terminal', 'file', 'mail_admins'],
            'level': 'DEBUG',
        },
    },
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
        'user': '1000/day'
    },
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'UNICODE_JSON': True,
}

SWAGGER_SETTINGS = {
    'doc_expansion': 'list',
}
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django registration redux
ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True  # Automatically log the user in.
LOGIN_REDIRECT_URL = '/'

SECRETS_FILE = os.path.join(BASE_DIR, '..', 'config.json')

with open(SECRETS_FILE) as f:
    SECRETS = json.loads(f.read())


def get_secret(setting, secrets=SECRETS):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


# should be configured for others
if sys.argv[1] != "test":
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = SECRETS["EMAIL_HOST"]
    EMAIL_PORT = '587'
    EMAIL_HOST_USER = SECRETS['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = SECRETS["EMAIL_HOST_PASSWORD"]
    EMAIL_USE_TLS = True
