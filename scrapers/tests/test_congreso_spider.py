import os
import unittest

from scrapers.manolo_scraper.spiders.congreso import CongresoSpider
from scrapers.tests.utils import fake_response_from_file


class TestCongresoSpider(unittest.TestCase):

    def setUp(self):
        self.spider = CongresoSpider()

    def test_parse_item(self):
        filename = os.path.join('data/congreso', '2021-08-24.json')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'18/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'RAFAEL PINTADO, HENRY HECTOR')
        self.assertEqual(item.get('host_title'), u'AUXILIAR')
        self.assertEqual(item.get('reason'), u'NORMAL')
        self.assertEqual(item.get('time_start'), u'17:46')
        self.assertEqual(item.get('id_document'), u'DNI/LE')
        self.assertEqual(item.get('id_number'), u'06794905')
        self.assertEqual(item.get('entity'), u'SIN INSTITUCION')
        self.assertEqual(item.get('host_name'), u'ZUÑIGA PAREDES, BLANCA LEONOR')
        self.assertEqual(item.get('office'), u'TERCERA VICEPRESIDENCIA')
        self.assertEqual(item.get('meeting_place'), u'PALACIO')
        self.assertEqual(item.get('location'), u'PALACIO : 229-E - TERCERA VICEPRESIDENCIA')
        self.assertEqual(item.get('time_end'), '21:15')
        self.assertEqual(item.get('institution'), u'congreso')
        self.assertEqual(item.get('date'), u'2015-08-18')

        number_of_items = 1 + sum(1 for x in items)

        self.assertEqual(number_of_items, 2)

    def test_start_request(self):
        self.spider.date_start = '2015-08-18'
        self.spider.date_end = '2015-08-19'
        requests = self.spider.start_requests()

        request = next(requests)
        self.assertEqual(
            request.url, 'https://wb2server.congreso.gob.pe/regvisitastransparencia/filtrar'
        )
        self.assertEqual(request.meta, {'date': '18/08/2015'})

        number_of_requests = sum(1 for _ in requests)
        self.assertEqual(number_of_requests, 1)
