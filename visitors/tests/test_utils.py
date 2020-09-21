from unittest.mock import MagicMock

from django.test import TestCase

from visitors.utils import get_user_profile, is_dni


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
