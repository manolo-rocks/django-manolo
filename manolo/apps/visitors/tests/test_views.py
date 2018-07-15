import datetime

from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from django.test.utils import override_settings
from django.contrib.auth.models import User
import haystack

from visitors.models import Visitor, Subscriber


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
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        # self.user = User.objects.get(username='admin')
        # self.user.set_password('pass')
        # self.user.save()
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

    def test_pagination(self):
        data = []
        for i in range(500):
            m = Visitor(full_name='Romulo', id=i, date=datetime.date(2015, 1, 1))
            data.append(m)
        Visitor.objects.bulk_create(data)

        # build index with our test data
        haystack.connections.reload('default')
        haystack.connections.reload('cazador')
        call_command('rebuild_index', interactive=False, verbosity=0)
        super(TestViews, self).setUp()

        c = self.client.get('/search/?q=romulo')
        expected = 'q=romulo&amp;page=25'
        self.assertTrue(expected in str(c.content))

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

    def test_search_date__client_has_valid_account(self):
        """can show recent record"""
        self.setup_subscriber()

        Visitor.objects.create(full_name='Romulo', date=datetime.datetime.today())

        # build index with our test data
        haystack.connections.reload('default')
        haystack.connections.reload('cazador')
        call_command('rebuild_index', interactive=False, verbosity=0)
        super(TestViews, self).setUp()

        today_str = datetime.datetime.today().strftime("%d/%m/%Y")

        self.client.login(username="testuser", password="12345")
        c = self.client.get('/search_date/?q=' + today_str)
        self.assertIn("ROMULO", str(c.content))

    def test_search_date__client_has_invalid_account__recent_record(self):
        """Cannot show recent record"""
        self.setup_subscriber()
        self.subscriber.credits = 0
        self.subscriber.save()

        Visitor.objects.create(full_name='Romulo', date=datetime.datetime.today())

        # build index with our test data
        haystack.connections.reload('default')
        call_command('rebuild_index', interactive=False, verbosity=0)
        super(TestViews, self).setUp()

        today_str = datetime.datetime.today().strftime("%d/%m/%Y")

        self.client.login(username="testuser", password="12345")
        c = self.client.get('/search_date/?q=' + today_str)
        self.assertNotIn("ROMULO", str(c.content))

    def test_search_date__client_has_invalid_account__old_record(self):
        """Can show old record"""
        self.setup_subscriber()
        self.subscriber.credits = 0
        self.subscriber.save()

        old_date = datetime.datetime.today() - datetime.timedelta(days=365)
        Visitor.objects.create(full_name='Romulo', date=old_date)

        # build index with our test data
        haystack.connections.reload('default')
        haystack.connections.reload('cazador')
        call_command('rebuild_index', interactive=False, verbosity=0)
        super(TestViews, self).setUp()

        old_date_str = old_date.strftime("%d/%m/%Y")

        self.client.login(username="john", password="smith")
        c = self.client.get('/search_date/?q=' + old_date_str)
        with open("/tmp/a.html", "w") as handle:
            handle.write(str(c.content))
        self.assertIn("ROMULO", str(c.content))

    def setup_subscriber(self):
        self.user = User.objects.create_superuser("john", "john@example.com", "smith")
        self.subscriber = Subscriber.objects.create(
            user=self.user, expiration=datetime.datetime.today(), credits=600)

