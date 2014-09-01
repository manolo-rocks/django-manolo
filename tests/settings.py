CRAWLERA_USER = ''
BASE_DIR = ''
SECRET_KEY = "Please do not spew DeprecationWarnings"

# settings for running tests.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'manolo_test.db',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'manolo',

    'tests.test_scraper',
]