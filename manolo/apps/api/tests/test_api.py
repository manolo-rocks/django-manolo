import datetime

from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.core.management import call_command
import haystack

from visitors.models import Visitor


TEST_INDEX = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'test_haystack',
        'EXCLUDED_INDEXES': ['cazador.search_indexes.CazadorIndex'],
    },
    'cazador': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'test_cazador',
        'EXCLUDED_INDEXES': ['visitors.search_indexes.VisitorIndex'],
    }
}


@override_settings(HAYSTACK_CONNECTIONS=TEST_INDEX)
class TestAPI(TestCase):
    def setUp(self):
        self.client = Client()

        data = []
        for i in range(500):
            m = Visitor(full_name='Romulo', id=i, date=datetime.date.today())
            data.append(m)
        Visitor.objects.bulk_create(data)

        # build index with our test data
        haystack.connections.reload('default')
        call_command('rebuild_index', interactive=False, verbosity=0)
        super(TestAPI, self).setUp()
        self.maxDiff = None

    def test_search_return_json(self):
        c = self.client.get('/api/search.json/romulo/')
        self.assertEqual(200, c.status_code)

    def test_search_return_json_with_pagination(self):
        c = self.client.get('/api/search.json/romulo/?page=2')
        self.assertEqual(200, c.status_code)

    def test_search_return_json_with_invalid_pagination(self):
        c = self.client.get('/api/search.json/romulo/?page=100')
        self.assertTrue('Invalid page' in str(c.content))
