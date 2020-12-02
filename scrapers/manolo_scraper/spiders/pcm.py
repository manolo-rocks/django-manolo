# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest

from .spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..utils import get_dni, make_hash


class PcmSpider(ManoloBaseSpider):
    name = 'pcm'
    institution_name = 'pcm'
    allowed_domains = ['visitas.pcm.gob.pe']
    base_url = 'https://visitas.pcm.gob.pe/visitas/Transparencia/Transparencia/Buscar_Visita'

    def initial_request(self, date):
        date_str = date.strftime("%d/%m/%Y")
        request = scrapy.FormRequest(
            self.base_url,
            formdata={
                'biCodMovPersona': '',
                'iCurrentPage': '1',
                'iPageSize': '25',
                'vFechFin': date_str,
                'vFechInicio': date_str,
                'vSortColumn': 'A.biCodMovVisita',
                'vSortOrder': 'asc',
            },
            meta={'date': date_str},
            callback=self.parse_initial_request,
        )
        return request

    def parse_initial_request(self, response):
        date_str = response.meta['date']
        page_count = response.json()['PageCount']
        for i in range(0, page_count):
            request = FormRequest(
                self.base_url,
                formdata={
                    'biCodMovPersona': '',
                    'iCurrentPage': str(i + 1),
                    'iPageSize': '25',
                    'vFechFin': date_str,
                    'vFechInicio': date_str,
                    'vSortColumn': 'A.biCodMovVisita',
                    'vSortOrder': 'asc',
                },
                meta={'date': date_str},
                callback=self.parse,
                dont_filter=True,
            )
            yield request

    def parse(self, response, **kwargs):
        date_str = response.meta['date']

        for item in response.json()['Items']:
            yield self.get_item(item['Row'], date_str)

    def get_item(self, item, date_str):
        try:
            document_identity = item[3].strip()
        except IndexError:
            document_identity = ''

        if document_identity != '':
            id_document, id_number = get_dni(document_identity)
        else:
            id_document = 'DNI'
            id_number = ''

        l = ManoloItem(
            institution=self.institution_name,
            date=date_str,
            full_name=item[2],
            entity=item[4],
            reason=item[5],
            location=item[6],
            office=item[8],
            meeting_place=item[9],
            host_name=item[7],
            time_start=item[10],
            time_end=item[11],
            id_document=id_document,
            id_number=id_number,
        )
        l = make_hash(l)
        return l
