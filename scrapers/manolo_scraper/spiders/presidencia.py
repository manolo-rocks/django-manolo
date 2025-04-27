# -*- coding: utf-8 -*-
import logging

from scrapy import FormRequest

from .spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import get_dni
from api.utils import make_hash


class PresidenciaSpider(ManoloBaseSpider):
    name = 'presidencia'
    allowed_domains = ['presidencia.gob.pe']
    base_url = 'http://appw.presidencia.gob.pe/visitas/transparencia'

    def initial_request(self, date):
        date_str = date.strftime('%d/%m/%Y')

        request = self._request_page(date_str, self.parse)

        return request

    def _request_page(self, date_str, callback):
        url = self.base_url + '/index_server.php?k=sbmtBuscar'
        request = FormRequest(
            url=url,
            meta={
                'date': date_str,
            },
            formdata={"valorCaja1": date_str},
            dont_filter=True,
            callback=callback,
        )
        request.meta['date'] = date_str
        return request

    def parse(self, response, **kwargs):
        rows = response.xpath('//tr')

        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        for row in rows:
            if len(row.xpath(".//td")) < 4:
                continue
            loader = ManoloItemLoader(item=ManoloItem(), selector=row)

            loader.add_value('institution', 'presidencia')
            loader.add_value('date', date)

            loader.add_xpath('full_name', './/td[3]/text()')

            loader.add_xpath('entity', './/td[5]/text()')

            loader.add_xpath('reason', './/td[6]/text()')
            loader.add_xpath('host_name', './/td[7]/text()')

            loader.add_xpath('time_start', './/td[9]/text()')
            loader.add_xpath('time_end', './/td[10]/text()')
            loader.add_xpath('meeting_place', './/td[11]/text()')

            document_identity = row.xpath('.//td[4]/text()').extract_first(default='')
            id_document, id_number = get_dni(document_identity)

            loader.add_value('id_number', id_number)
            loader.add_value('id_document', id_document)

            office_title = row.xpath('.//td[8]/text()').extract_first(default='')
            office_title = office_title.split('-')

            warnings = []
            try:
                loader.add_value('office', office_title[0])
            except IndexError:
                warnings.append("No office for item: ")

            try:
                loader.add_value('title', office_title[1])
            except IndexError:
                warnings.append("No title for item: ")

            item = loader.load_item()
            item = make_hash(item)

            if warnings:
                for i in warnings:
                    logging.warning("{0}{1}".format(i, item))

            yield item
