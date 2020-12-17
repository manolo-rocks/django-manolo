# -*- coding: utf-8 -*-
import scrapy

from scrapers.manolo_scraper.spiders.spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash, get_dni


class MinceturSpider(ManoloBaseSpider):
    name = 'mincetur'
    allowed_domains = ["mincetur.gob.pe"]
    base_url = "http://consultasenlinea.mincetur.gob.pe/visitaspublico/Visitas/FrmVisitantes.aspx"

    def initial_request(self, date):
        return scrapy.http.Request(
            url=self.base_url,
            meta={
                'date_str': date.strftime("%d/%m/%Y"),
            },
            dont_filter=True,
            callback=self.parse_initial_request,
        )

    def parse_initial_request(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                'tbFecha': response.meta['date_str'],
            },
            meta={
                'date_str': response.meta['date_str'],
            },
            dont_filter=True,
            callback=self.parse_pages,
        )

    def parse_pages(self, response):
        number_of_pages = int(response.xpath(
            "//span[@id='gvVisitante_lblTotalPaginas']/text()",
        ).extract_first(default=1))

        for page in range(number_of_pages):
            yield scrapy.FormRequest.from_response(
                response,
                formdata={
                    'ScriptManager1': 'UpDatos|gvVisitante$ctl23$ibPagIr',
                    'tbFecha': response.meta['date_str'],
                    'gvVisitante$ctl23$tbPagIr': str(page + 1),
                    'gvVisitante$ctl23$ibPagIr.x': "6",
                    'gvVisitante$ctl23$ibPagIr.y': '12',
                },
                meta={
                    'date_str': response.meta['date_str'],
                },
                dont_filter=True,
                callback=self.parse_item,
            )

    def parse_item(self, response):
        date = self.get_date_item(response.meta['date_str'], '%d/%m/%Y')
        rows = response.xpath("//tr")
        for row in rows:
            if len(row.xpath('.//td')) != 6:
                continue
            l = ManoloItemLoader(item=ManoloItem(), selector=row)

            l.add_value('institution', 'mincetur')
            l.add_value('date', date)


            date_time = row.xpath('./td[2]/text()').extract_first().split()
            l.add_value('time_start', date_time[1])

            full_name = row.xpath('./td[3]/span/@title').extract_first()
            l.add_value('full_name', full_name)

            entity = row.xpath('./td[3]/text()').extract()[-1]
            l.add_value('entity', entity)

            id_document, id_number = get_dni(row.xpath('./td[3]/span/text()').extract()[1])
            l.add_value('id_document', id_document)
            l.add_value('id_number', id_number)

            reason = row.xpath('./td[4]/text()').extract()[0]
            l.add_value('reason', reason)

            meeting_place = row.xpath('./td[4]/text()').extract()[1]
            l.add_value('meeting_place', meeting_place)

            host_name = row.xpath('./td[5]/span/text()').extract()[0]
            l.add_value('host_name', host_name)

            host_title = row.xpath('./td[5]/span/text()').extract()[1]
            l.add_value('host_title', host_title)

            office = row.xpath('./td[5]/span/text()').extract()[2]
            l.add_value('office', office)

            time_end = row.xpath('./td[6]/span/text()').extract_first()
            l.add_value('time_end', time_end)

            item = l.load_item()
            item = make_hash(item)
            yield item
