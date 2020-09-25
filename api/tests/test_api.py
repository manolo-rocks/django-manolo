import datetime

from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from visitors.models import Visitor


class TestAPI(TestCase):
    def setUp(self):
        self.client = Client()

        data = []
        for i in range(500):
            m = Visitor(full_name='Romulo', id=i, date=datetime.date(2015, 1, 1))
            data.append(m)
        Visitor.objects.bulk_create(data)

        # build index with our test data
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
