from .base import *

print('Testing')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'manolo_test.db',
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'haystack',
        'EXCLUDED_INDEXES': ['cazador.search_indexes.CazadorIndex'],
    },
    'cazador': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'cazador',
        'EXCLUDED_INDEXES': ['visitors.search_indexes.VisitorIndex'],
    }
}
