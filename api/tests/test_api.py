import datetime

from django.test import TestCase, override_settings
from django.test.client import Client

from visitors.models import Visitor


@override_settings(SECURE_SSL_REDIRECT=False)
class TestAPI(TestCase):
    def setUp(self):
        self.client = Client()

        data = []
        for i in range(500):
            m = Visitor(
                full_name="Romulo",
                id=i,
                date=datetime.date(2015, 1, 1),
                created=datetime.datetime.now(tz=datetime.timezone.utc),
                modified=datetime.datetime.now(tz=datetime.timezone.utc),
            )
            data.append(m)
        Visitor.objects.bulk_create(data)
        # another query to update full_search explicitly since
        # bulk_create does not invoke the save method
        Visitor.objects.update(full_search=Visitor.get_full_search_vector())

        # build index with our test data
        self.maxDiff = None

    def test_search_return_json(self):
        c = self.client.get("/api/search.json/romulo/")
        self.assertEqual(404, c.status_code)

    def test_search_return_json_with_pagination(self):
        c = self.client.get("/api/search.json/romulo/?page=2")
        self.assertEqual(404, c.status_code)

    def test_search_return_json_with_invalid_pagination(self):
        c = self.client.get("/api/search.json/romulo/?page=100")
        self.assertFalse("Invalid page" in str(c.content))
