import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from visitors.models import Subscriber
from visitors.views import query_is_dni


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.maxDiff = None

    def test_index(self):
        c = self.client.get('/')
        self.assertEqual(200, c.status_code, 'Status code')
        self.assertTrue('0</b></span> registros de visitas' in str(c.content), 'Number of records in db.')

    def test_about(self):
        c = self.client.get('/about/')
        self.assertEqual(200, c.status_code, 'Status code')

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

    def test_search_view__user_1_credits(self):
        self.setup_subscriber()
        self.subscriber.credits = 1
        self.subscriber.save()
        self.client.login(username="john", password="smith")
        c = self.client.get('/search_date/?q=2010-01-01')
        self.assertIn("luego de usar 1", str(c.content))

    def setup_subscriber(self):
        self.user = User.objects.create_superuser("john", "john@example.com", "smith")
        self.subscriber = Subscriber.objects.create(
            user=self.user, expiration=datetime.datetime.today(), credits=600)

    def test_query_is_dni(self):
        items = [
            {
                'query': 'yoni pacheco',
                'expected': False,
            },
            {
                'query': '10468395',
                'expected': True,
            },
            {
                'query': 'yoni pacheco 10468395',
                'expected': False,
            },
            {
                'query': '24779433-s',
                'expected': True,
            },
        ]
        for item in items:
            result = query_is_dni(item['query'])
            self.assertEqual(result, item['expected'])
