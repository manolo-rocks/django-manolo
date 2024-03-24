import math

import scrapy

from .spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash, get_dni

# url: http://intranet.minem.gob.pe/GESTION/visitas_pcm


class MinemSpiderOld(ManoloBaseSpider):
    name = 'minem'
    allowed_domains = ['http://intranet.minem.gob.pe']

    NUMBER_OF_PAGES_PER_PAGE = 20

    def initial_request(self, date):
        date_str = date.strftime("%d/%m/%Y")
        request = self.make_form_request(date_str, self.parse_pages, 1)
        return request

    def make_form_request(self, date_str, callback, page_number):
        page_url = 'http://intranet.minem.gob.pe/GESTION/visitas_pcm/Busqueda/DMET_html_SelectMaestraBuscador'

        start_from_record = self.NUMBER_OF_PAGES_PER_PAGE * (page_number - 1) + 1

        params = {
            'TXT_FechaVisita_Inicio': date_str,
            'Ls_Pagina': str(start_from_record),
            'Li_ResultadoPorPagina': '20',
            'FlgBuscador': '1',
            'Ls_ParametrosBuscador': 'TXT_FechaVisita_Inicio=10/08/2015|Ls_Pagina={}'.format(start_from_record),  # noqa
        }

        request = scrapy.FormRequest(url=page_url, formdata=params,
                                     meta={'date': date_str},
                                     dont_filter=True,
                                     callback=callback)
        return request

    def parse_pages(self, response):
        total_of_records = response.css('#HID_CantidadRegistros').xpath('./@value').extract_first(default=1)  # noqa
        total_of_records = int(total_of_records)
        number_of_pages = self.get_number_of_pages(total_of_records)

        for page in range(1, number_of_pages + 1):
            request = self.make_form_request(response.meta['date'], self.parse, page)
            yield request

    def get_number_of_pages(self, total_of_records):
        return int(math.ceil(total_of_records / float(self.NUMBER_OF_PAGES_PER_PAGE)))

    def parse(self, response):
        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        rows = response.xpath("//tr")

        for row in rows:
            loader = ManoloItemLoader(item=ManoloItem(), selector=row)

            loader.add_value('institution', 'minem')
            loader.add_value('date', date)

            loader.add_xpath('full_name', './td[3]/center/text()')
            loader.add_xpath('entity', './td[5]/center/text()')
            loader.add_xpath('reason', './td[6]/center/text()')
            loader.add_xpath('host_name', './td[7]/center/text()')
            loader.add_xpath('office', './td[8]/center/text()')
            loader.add_xpath('meeting_place', './td[9]/center/text()')
            loader.add_xpath('time_start', './td[10]/center/text()')
            loader.add_xpath('time_end', './td[11]/center/text()')

            document_identity = row.xpath('td[4]/center/text()').extract_first(default='')

            id_document, id_number = get_dni(document_identity)

            loader.add_value('id_document', id_document)
            loader.add_value('id_number', id_number)

            item = loader.load_item()

            item = make_hash(item)

            yield item
