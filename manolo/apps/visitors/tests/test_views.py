from django.test import TestCase
from django.test.client import Client


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        c = self.client.get('/')
        self.assertEqual(200, c.status_code)

    def test_search(self):
        c = self.client.get('/search/?q=romulo')
        self.assertEqual(200, c.status_code)

    def test_search_date(self):
        c = self.client.get('/search_date/?q=30/05/2014')
        self.assertEqual(200, c.status_code)

    def test_search_date_empty(self):
        c = self.client.get('/search_date/?q=')
        self.assertEqual(302, c.status_code)

    def test_search_date_empty2(self):
        c = self.client.get('/search_date/')
        self.assertEqual(302, c.status_code)

    def test_search_date_invalid(self):
        c = self.client.get('/search_date/?q=30/05/20120302')
        self.assertEqual(200, c.status_code)

    def test_search_date_invalid2(self):
        c = self.client.get('/search_date/?q=30/05/2012&page=10')
        self.assertEqual(404, c.status_code)

    def test_search_date_invalid3(self):
        c = self.client.get('/search_date/?q=30/05/2012&page=0')
        self.assertEqual(404, c.status_code)

    def test_search_date_invalid4(self):
        c = self.client.get('/search_date/?q=30/05/2012&page=abadca')
        self.assertEqual(404, c.status_code)

    def test_search_return_json(self):
        c = self.client.get('/search/?q=romulo&json')
        self.assertEqual(200, c.status_code)

    def test_search_return_json_with_pagination(self):
        c = self.client.get('/search/?q=romulo&page=1&json')
        self.assertEqual(200, c.status_code)

    def test_search_return_json_with_invalid_pagination(self):
        c = self.client.get('/search/?q=romulo&page=100&json')
        self.assertEqual(404, c.status_code)
