from django.test import TestCase

from visitors.utils import is_dni, Paginator


class TestUtils(TestCase):

    def test_is_dni(self):
        items = [
            # input, expected
            ('bla', False),
            ('0989', False),
            ('0989', False),
            ('09976110', True),
            ('9976110', True),
        ]
        for item in items:
            result = is_dni(item[0])
            self.assertEqual(result, item[1])


class TestPaginator(TestCase):
    def test_paginator_with_less_than_10_pages_should_return_all_pages(self):
        results = list(range(0, 199))
        results_per_page = 20
        paginator = Paginator(results, results_per_page)
        paginator.page(1)
        self.assertEqual(paginator.paginate_sections(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_paginator_with_more_than_10_pages_should_hide_some_of_them(self):
        results = list(range(0, 300))
        results_per_page = 20
        paginator = Paginator(results, results_per_page)
        paginator.page(1)
        self.assertEqual(paginator.paginate_sections(), [1, 2, 3, 4, 5, None, 11, 12, 13, 14, 15])
