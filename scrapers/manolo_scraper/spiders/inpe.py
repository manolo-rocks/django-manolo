# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request, FormRequest

from scrapers.manolo_scraper.spiders.spiders import ManoloBaseSpider
from ..item_loaders import ManoloItemLoader
from ..items import ManoloItem
from ..utils import make_hash, get_dni


class INPESpider(ManoloBaseSpider):
    name = 'inpe'
    allowed_domains = [
        'apps.inpe.gob.pe',
    ]

    def initial_request(self, date):
        date_str = date.strftime('%d/%m/%Y')
        url = f'https://apps.inpe.gob.pe/VisitasadmInpe/CargarTablaVisitaJSON?FechaVisita={date_str}&local=-1'
        requests = FormRequest(
            url,
            meta={'date': date_str},
            dont_filter=True,
            callback=self.parse,
        )
        return requests

    def parse(self, response, **kwargs):
        data = json.loads(response.text)['aaData']
        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        for row in data:
            l = ManoloItemLoader(item=ManoloItem(), selector=row)

            l.add_value('institution', 'inpe')
            l.add_value('date', date)

            l.add_value('full_name', row[1])

            dni_str, dni_number = get_dni(row[2])
            l.add_value('id_document', dni_str)
            l.add_value('id_number', dni_number)
            l.add_value('entity', row[3])
            l.add_value('time_start', row[4])
            l.add_value('time_end', row[5])
            l.add_value('reason', row[6])
            l.add_value('host_name', row[7])
            l.add_value('host_title', row[8])
            l.add_value('office', row[9])
            l.add_value('location', row[10])
            item = l.load_item()
            item = make_hash(item)
            yield item
