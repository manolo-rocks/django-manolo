import os

import environ
from pathlib import Path

from kombu import Exchange, Queue

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / 'manolo'

env = environ.Env()

# OS environment variables take precedence over variables from .env
env.read_env(str(ROOT_DIR / '.env'))

# PATH vars
DEBUG = env.bool("DJANGO_DEBUG", True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'manolo',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'db',
        'PORT': 5432,
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

ADMINS = (
    ('AniversarioPeru', 'aniversarioperu1@gmail.com'),
)
MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
TIME_ZONE = 'America/Lima'

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

# Absolute filesystem path to the directory for user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = str(ROOT_DIR / 'docker/devdata/media/')
LOG_DIR = str(ROOT_DIR / 'docker/devdata/logs/')
STATIC_ROOT = str(ROOT_DIR / 'docker/devdata/static/')

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
    str(APPS_DIR / '../media'),
    str(APPS_DIR / "assets"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR / "templates")],
        'OPTIONS': {
            # needed for building sitemaps
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'manolo.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'manolo.wsgi.application'

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',
]

THIRD_PARTY_APPS = [
    'bootstrap4',
    'bootstrap_themes',
    'crispy_forms',
    'registration',
    'rest_framework',
    'rest_framework_api_key',
    'rest_framework_swagger',
    'drf_yasg',
]
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

LOCAL_APPS = [
    'visitors',
    'api',
    'cazador',
    'scrapers',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

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
            'filename': LOG_DIR + '/manolo.rocks.main.log',
            'formatter': 'verbose',
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + '/manolo.rocks.main.debug.log',
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
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
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

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django registration redux
ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True  # Automatically log the user in.
LOGIN_REDIRECT_URL = '/'

# celery - redis
BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERY_TASK_ALWAYS_EAGER = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'aniversarioperu1@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
ASYNC_MODE = True
