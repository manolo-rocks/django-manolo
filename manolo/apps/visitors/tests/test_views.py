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
