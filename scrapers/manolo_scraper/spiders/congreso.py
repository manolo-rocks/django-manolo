# -*- coding: utf-8 -*-
import re
import json

from scrapy import Request

from scrapers.manolo_scraper.spiders.spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..utils import make_hash


class CongresoSpider(ManoloBaseSpider):
    name = 'congreso'
    allowed_domains = ['wb2server.congreso.gob.pe']
    base_url = 'https://wb2server.congreso.gob.pe/regvisitastransparencia/filtrar'

    def initial_request(self, date):
        date_str = date.strftime("%d/%m/%Y")
        payload = {
            'empleadoCampo': '1',
            'empleadoNombres': '',
            'fechaDesde': date.strftime('%Y-%m-%d'),
            'fechaHasta': date.strftime('%Y-%m-%d'),
            'visitanteCampo': '1',
            'visitanteNombres': ''
        }

        # This initial request always hits the current page of the date.
        request = Request(
            url=self.base_url,
            method='POST',
            body=json.dumps(payload),
            meta={
                'date': date_str,
            },
            dont_filter=True,
            callback=self.parse,
        )
        return request

    def parse(self, response):
        res_json = response.json()

        for record in res_json:
            date_str = self.get_date_item(response.meta['date'], '%d/%m/%Y')

            # extract hora vista from fecha visita
            fecha_visita_orig = record.get('fechaVisitaRecepcion', '') or ''
            fecha_visita = fecha_visita_orig.split(' ')
            try:
                hora_visita = fecha_visita[1]
            except IndexError:
                hora_visita = fecha_visita_orig

            location = record.get('ubicacion', '') or ''
            location = re.sub(r'\s+', ' ', location)

            item = ManoloItem(
                institution=self.name,
                date=date_str,
                full_name=record.get('entidadVisitanteNombreCompleto', '') or '',
                time_start=hora_visita,
                id_document=record.get('entidadVisitanteTipoDocumento', '') or '',
                id_number=record.get('entidadVisitanteDocumento', '') or '',
                entity=record.get('entidad', '') or '',
                reason=record.get('motivo', '') or '',
                host_name=record.get('empleado', '') or '',
                host_title=record.get('cargo', '') or '',
                location=location,
                office=record.get('centroCostoNombre', '') or '',
                meeting_place=record.get('edificio', '') or '',
                time_end=record.get('fechaVisitaTermino', '') or '',
            )

            item = make_hash(item)
            yield item
