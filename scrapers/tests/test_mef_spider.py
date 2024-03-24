import os
import unittest

from scrapers.manolo_scraper.spiders.mef import MefSpider
from scrapers.tests.utils import fake_response_from_file


class TestMefSpider(unittest.TestCase):

    def setUp(self):
        self.spider = MefSpider()

    def test_parse_item(self):
        filename = os.path.join('data/mef', 'test_file.json')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'18/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'MEJIA BENDEZU EMERSON JACOB')
        self.assertEqual(item.get('host_title'), u'Asesor')
        self.assertEqual(item.get('reason'), u'Reunión de trabajo')
        self.assertEqual(item.get('time_start'), u'09:30')
        self.assertEqual(item.get('id_document'), None)
        self.assertEqual(item.get('id_number'), None)
        self.assertEqual(item.get('entity'), u'Aeropuertos del Perú SA')
        self.assertEqual(item.get('host_name'), u'RAMIREZ CASTILLO DIANA ROSALIA')
        self.assertEqual(item.get('office'), u'Equipo Especializado de Seguimiento de la Inversión')
        self.assertEqual(item.get('meeting_place'), u'Sala Técnica 2')
        self.assertEqual(item.get('location'), None),
        self.assertEqual(item.get('time_end'), '10:50')
        self.assertEqual(item.get('institution'), u'mef')

        number_of_items = 1 + sum(1 for x in items)

        self.assertEqual(number_of_items, 10)
