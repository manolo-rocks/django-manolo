import unittest

from .utils import shrink_url_in_string


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_shrink_url_in_string(self):
        my_string = "Carlos Fernando Raffo Arce http://ot.minjus.gob.pe:8080/sisca_web/DeudoresWebAction_verDeudorWeb.action?deudor.id=7683"
        expected = "Carlos Fernando Raffo Arce  <a href='http://ot.minjus.gob.pe:8080/sisca_web/DeudoresWebAction_verDeudorWeb.action?deudor.id=7683'>http://ot.minjus.gob.pe...</a>"
        result = shrink_url_in_string(my_string)
        self.assertEqual(expected, result)
