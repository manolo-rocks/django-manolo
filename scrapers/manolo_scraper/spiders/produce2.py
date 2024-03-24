# -*- coding: utf-8 -*-
import json

import scrapy

from .spiders import ManoloBaseSpider
from ..item_loaders import ManoloItemLoader
from ..items import ManoloItem
from ..utils import make_hash


class ProduceSpider2(ManoloBaseSpider):
    name = 'produce2'
    allowed_domains = ['www.produce.gob.pe']

    def initial_request(self, date):
        date_str = date.strftime("%d/%m/%Y")
        display_end = 10_000
        url = (
            'https://www.produce.gob.pe/images/produce/transparencia/visitas/ajax/visitas.php?'
            'sEcho=4&iColumns=13&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&'
            f'iDisplayLength={display_end}&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true'  # noqa
            '&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&mDataProp_2=2&sSearch_2=&'
            'bRegex_2=false&bSearchable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&'
            'bSearchable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&'
            'mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&mDataProp_6=6&sSearch_6=&'
            'bRegex_6=false&bSearchable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&'
            'bSearchable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&'
            'mDataProp_9=9&sSearch_9=&bRegex_9=false&bSearchable_9=true&mDataProp_10=10&sSearch_10=&'  # noqa
            'bRegex_10=false&bSearchable_10=true&mDataProp_11=11&sSearch_11=&bRegex_11=false&'
            'bSearchable_11=true&mDataProp_12=12&sSearch_12=&bRegex_12=false&bSearchable_12=true&'
            'sSearch=&bRegex=false&dni=&visitante=&entidad=&funcionario=&sede=0&motivo=0&'
            f'fecha_inicio={date_str}&fecha_fin={date_str}&_=1607905978616'
        )
        request = scrapy.Request(url, callback=self.parse)
        request.meta['date'] = date_str

        return request

    def parse(self, response, **kwargs):
        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')
        response_json = json.loads(response.text)
        rows = response_json['aaData']

        for row in rows:
            loader = ManoloItemLoader(item=ManoloItem(), selector=row)

            loader.add_value('institution', 'produce')
            loader.add_value('date', date),
            loader.add_value('full_name', row['VISITANTE'])
            try:
                loader.add_value('id_document', row['DOCUMENTO'].split(' ')[0])
            except IndexError:
                loader.add_value('id_document', 'DNI')

            loader.add_value('id_number', row['NUMERO_DOCUMENTO'])
            loader.add_value('reason', row['MOTIVO'])
            loader.add_value('entity', row['ENTIDAD'])
            loader.add_value('host_name', row['FUNCIONARIO'])
            loader.add_value('office', row['DEPENDENCIA'])
            loader.add_value('time_end', row['HORA_SALIDA'])
            loader.add_value('time_start', row['HORA_INGRESO'])
            loader.add_value('location', row['SEDE'])
            loader.add_value('host_title', row['DESCRIPCION_CARGO'])

            item = loader.load_item()
            item = make_hash(item)

            yield item
