# -*- coding: utf-8 -*-
import scrapy

from .spiders import SireviSpider, ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import get_dni


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
                'iCurrentPage': 1,
                'iPageSize': 25,
                'vFechFin': date_str,
                'vFechInicio': date_str,
                'vSortColumn': 'A.biCodMovVisita',
                'vSortOrder': 'asc',
            },
            callback=self.parse)

        request.meta['date'] = date_str

        return request

    def get_item(self, data, date_str, row):
        l = ManoloItemLoader(item=ManoloItem(), selector=row)

        l.add_value('institution', self.institution_name)
        l.add_value('date', date_str)
        l.add_xpath('full_name', './td[2]/text()')
        l.add_xpath('entity', './td[4]/text()')
        l.add_xpath('reason', './td[5]/text()')
        l.add_xpath('location', './td[6]/text()')
        l.add_xpath('host_name', './td[7]/text()')
        l.add_xpath('office', './td[8]/text()')
        l.add_xpath('meeting_place', './td[9]/text()')
        l.add_xpath('time_start', './td[10]/text()')
        l.add_xpath('time_end', './td[11]/text()')

        try:
            document_identity = data[2].strip()
        except IndexError:
            document_identity = ''

        if document_identity != '':
            id_document, id_number = get_dni(document_identity)

            l.add_value('id_document', id_document)
            l.add_value('id_number', id_number)

        return l.load_item()
