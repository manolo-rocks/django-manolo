# -*- coding: utf-8 -*-
import json

import scrapy

from scrapers.manolo_scraper.spiders.spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash, get_dni


class MidisSpider(ManoloBaseSpider):
    name = 'midis'
    allowed_domains = ['sdv.midis.gob.pe']
    NUMBER_OF_PAGES_PER_PAGE = 20
    base_url = "http://sdv.midis.gob.pe/Sis_TransparenciaVisita/Transparencia/Transparencia/Buscar_Visita"

    def initial_request(self, date):
        date_str = date.strftime("%d/%m/%Y")

        # This initial request always hits the current page of the date.
        request = scrapy.FormRequest(
            url=self.base_url,
            meta={
                'date': date_str,
            },
            formdata={
                'biCodMovPersona': '',
                'iCurrentPage': '1',
                'iPageSize': '2000000',
                'vFechFin': date_str,
                'vFechInicio': date_str,
                'vSortColumn': 'biCodMovVisita',
                'vSortOrder': 'asc',
            },
            dont_filter=True,
            callback=self.parse)

        return request

    def parse(self, response, **kwargs):
        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')
        data = json.loads(response.text)

        for item in data['Items']:
            row = item['Row']

            dni = row[3]
            id_document, id_number = get_dni(dni)

            l = ManoloItemLoader(item=ManoloItem(), selector=row)
            l.add_value('date', date)
            l.add_value('institution', self.name)
            l.add_value('full_name', row[2])
            l.add_value('id_document', id_document)
            l.add_value('id_number', id_number)
            l.add_value('entity', row[4])
            l.add_value('reason', row[5])
            l.add_value('host_name', row[6])
            l.add_value('host_title', row[7])
            l.add_value('office', row[8])
            l.add_value('meeting_place', row[9])
            try:
                l.add_value('time_start', row[10].strip())
            except Exception:
                l.add_value('time_start', row[10])

            try:
                l.add_value('time_end', row[11].strip().replace(' ', ''))
            except Exception:
                l.add_value('time_end', row[11])

            item = l.load_item()
            item = make_hash(item)

            yield item
