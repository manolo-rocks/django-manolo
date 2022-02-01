import logging

from scrapy.http import FormRequest, Request

from scrapers.manolo_scraper.spiders.spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash


class JusticiaUpTo202108Spider(ManoloBaseSpider):
    """Run this scraper in a peruvian server because the minjus blocks non
    peruvian ips
    """
    name = 'justicia_up_to_2021_08'
    allowed_domains = ['visitas.minjus.gob.pe']
    base_url = 'https://visitas.minjus.gob.pe/visita_web/consulta_buscarVisitas'

    def initial_request(self, date):
        date_str = date.strftime('%d/%m/%Y')
        request = FormRequest(
            url=self.base_url,
            formdata={
                'visita.visitanteNombres': '',
                'visita.personalNombre': '',
                'visita.oficinaNombre': '',
                'visita.sedeId': '00',
                'fechaDesde': date_str,
                'fechaHasta': date_str,
                'ano': '0000',
                'mes': '00',
                'correcto': '0',
                'visita.ano': '',
                'visita.mes': '',
                'visita.fechaIngreso': '',
                'paginaNueva': '0',
                'paginaNueva2': '0',
                'visita.visitanteId': '0',
                'visita.personalId': '0',
                'visita.oficinaId': '0',
            },
            meta={
                'date': date_str,
                'page_current': 0,
            },
            callback=self.parse_initial_request,
        )
        return request

    def parse_initial_request(self, response):
        date_str = response.meta['date']
        items = self.parse(response)

        item_count = 0
        for item in items:
            item_count += 1
            yield item

        if item_count:
            page_current = response.meta['page_current'] + 1
            request = FormRequest(
                self.base_url,
                formdata={
                    'visita.visitanteNombres': '',
                    'visita.personalNombre': '',
                    'visita.oficinaNombre': '',
                    'visita.sedeId': '00',
                    'fechaDesde': date_str,
                    'fechaHasta': date_str,
                    'ano': '0000',
                    'mes': '00',
                    'correcto': '0',
                    'visita.ano': '',
                    'visita.mes': '',
                    'visita.fechaIngreso': '',
                    'paginaActual': str(page_current),
                    'paginaNueva': str(page_current),
                    'paginaNueva2': '0',
                    'visita.visitanteId': '0',
                    'visita.personalId': '0',
                    'visita.oficinaId': '0',
                },
                meta={
                    'date': date_str,
                    'page_current': page_current,
                },
                callback=self.parse_initial_request,
            )
            yield request

    def parse(self, response):
        rows = response.xpath('//table/tr')
        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        for row in rows:
            warnings = []
            l = ManoloItemLoader(item=ManoloItem(), selector=row)

            l.add_value('institution', 'minjus')
            l.add_value('date', date)

            l.add_xpath('full_name', './/td[4]/br/preceding-sibling::node()/self::text()')

            l.add_xpath('entity', './/td[4]/b/following-sibling::node()/self::text()')

            l.add_xpath('reason', './/td[6]/br/preceding-sibling::node()/self::text()')
            l.add_xpath('host_name', './/td[7]/br/preceding-sibling::node()/self::text()')
            l.add_xpath('office', './/td[7]/b/following-sibling::node()/self::text()')

            l.add_xpath('location', './/td[1]/text()')

            l.add_xpath('id_document', './/td[5]/br/preceding-sibling::node()/self::text()')
            try:
                l.add_xpath('id_number', './/td[5]/br/following-sibling::node()/self::text()')
            except KeyError as e:
                warnings.append("No id number, error: {} for item: ".format(e))

            time_start_time_end = row.xpath(
                './/td[2]/div/br/following-sibling::node()/self::text()',
            ).extract_first(default='')

            time_start_time_end = time_start_time_end.split('-')

            try:
                l.add_value('time_start', time_start_time_end[0])
            except IndexError:
                warnings.append("No time_start for item: ")

            try:
                l.add_value('time_end', time_start_time_end[1])
            except IndexError:
                warnings.append("No time_end for item: ")

            item = l.load_item()
            item = make_hash(item)

            if warnings:
                for i in warnings:
                    logging.warning("{0}{1}".format(i, item))

            yield item
