# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request, FormRequest

from scrapers.manolo_scraper.spiders.spiders import ManoloBaseSpider
from ..item_loaders import ManoloItemLoader
from ..items import ManoloItem
from ..utils import make_hash


class INPESpider(ManoloBaseSpider):
    name = 'inpe'
    allowed_domains = [
        'apps.inpe.gob.pe',
    ]

    def initial_request(self, date):
        date_str = date.strftime('%d/%m/%Y')
        url = f'https://apps.inpe.gob.pe/VisitasadmInpe/CargarTablaVisitaJSON?FechaVisita={date_str}&local=-1'
        requests = Request(
            url,
            meta={'date': date_str},
            dont_filter=True,
            callback=self.parse_initial_request,
        )
        print('requests', requests)
        return requests

    def parse_initial_request(self, response):
        date = response.meta['date']
        data = json.loads(response.text)
        record_count = data['iTotalDisplayRecords']

        steps = list(range(0, record_count, 8))
        requests = []
        for i in steps:
            print(i, response.url)
            params = {'start': i, 'length': 8}
            print(params)
            request = FormRequest.from_response(
                response,
                formdata=params,
                dont_filter=True,
                callback=self.parse,
            )
            requests.append(request)
        return requests

    def _request_initial_date_page(self, response, date_str, callback):
        data = json.loads(response.text)
        record_count = data['iTotalDisplayRecords']

        steps = list(range(0, record_count, 8))

        for i in steps:
            print(i, response.url)
            params = {'start': i, 'length': 8}
            print(params)
            request = FormRequest.from_response(
                response,
                formdata=params,
                callback=self.hola,
            )
            yield request

    def hola(self, response):
        print('hola')

    def parse(self, response, **kwargs):
        print('**** response')
        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        rows = response.xpath('//tr')

        for row in rows:
            data = row.xpath('td')

            if len(data) > 7:
                l = ManoloItemLoader(item=ManoloItem(), selector=row)

                l.add_value('institution', 'inpe')
                l.add_value('date', date)

                l.add_xpath('full_name', './td[3]/p/text()')
                l.add_xpath('id_document', './td[4]/p/text()')

                id_document = l.get_output_value('id_document')

                if id_document is None:
                    l.replace_value('id_document', 'Otros')

                l.add_xpath('id_number', './td[5]/p/text()')
                l.add_xpath('entity', './td[6]/p/text()')
                l.add_xpath('reason', './td[7]/p/text()')
                l.add_xpath('host_name', './td[8]/p/text()')

                # Add conditional, don't accept "---"
                l.add_xpath('host_title', './td[9]/p/text()')

                l.add_xpath('office', './td[10]/p/text()')

                l.add_xpath('time_start', './td[2]/text()')
                l.add_xpath('time_end', './td[11]/text()')

                item = l.load_item()

                item = make_hash(item)

                yield item
