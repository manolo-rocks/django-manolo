from unittest.mock import MagicMock

from django.test import TestCase

from visitors.utils import get_user_profile, is_dni, Paginator


class TestUtils(TestCase):

    def test_get_user_profile__user_is_authenticated_has_0_credits(self):
        mock_subscriber = MagicMock()
        mock_subscriber.credits = 0

        mock_request = MagicMock()
        mock_request.user.is_authenticated.return_value = True
        mock_request.user.subscriber = mock_subscriber
        result = get_user_profile(mock_request)
        self.assertEqual(True, result["expired"])
        self.assertEqual(False, result["about_to_expire"])
        self.assertEqual(0, result["credits"])

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
