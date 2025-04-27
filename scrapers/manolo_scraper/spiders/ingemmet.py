import scrapy

from scrapers.manolo_scraper.spiders.spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import get_dni
from api.utils import make_hash


class IngemmetSpider(ManoloBaseSpider):
    name = 'ingemmet'
    allowed_domains = ['ingemmet.gob.pe']
    base_url = 'http://www.ingemmet.gob.pe/form/ListaVisitas.aspx'
    institution_name = 'ingemmet'
    DATE_REQUEST_FORMAT = "%d/%m/%Y"

    def initial_request(self, date):
        date_str = date.strftime(self.DATE_REQUEST_FORMAT)

        # This initial request always hit the current page of the date.
        request = scrapy.Request(
            url=self.base_url,
            meta={
                'date': date_str,
            },
            dont_filter=True,
            callback=self.parse_initial_request,
        )
        return request

    def parse_initial_request(self, response):
        date = response.meta['date']
        request = scrapy.FormRequest.from_response(
            response,
            formdata={
                'txtFechaVisita': date,
                'btnListar': 'Listar',
            },
            dont_filter=True,
            callback=self.parse_page,
        )
        request.meta['date'] = date
        yield request

    def parse_page(self, response):
        items = self.parse(response)

        # Parse items from the first page
        for item in items:
            yield item

    def parse(self, response):
        date = self.get_date_item(response.meta['date'], self.DATE_REQUEST_FORMAT)

        rows = response.xpath('//tr')

        for row in rows:
            cells = row.xpath("./td")
            if len(cells) > 8:
                loader = ManoloItemLoader(item=ManoloItem(), selector=row)
                loader.add_value('institution', self.institution_name)
                loader.add_value('date', date)

                id_document, id_number = get_dni(cells[2].xpath("text()").extract_first())

                loader.add_value('id_document', id_document)
                loader.add_value('id_number', id_number)

                loader.add_xpath('full_name', './/td[2]/text()')
                loader.add_xpath('entity', './/td[4]/text()')
                loader.add_xpath('reason', './/td[5]/text()')
                loader.add_xpath('host_name', './/td[6]/text()')
                loader.add_xpath('office', './/td[7]/text()')

                loader.add_xpath('time_start', './/td[8]/text()')
                loader.add_xpath('time_end', './/td[9]/text()')

                item = loader.load_item()
                item = make_hash(item)
                yield item
