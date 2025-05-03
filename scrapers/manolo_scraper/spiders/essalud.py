from scrapy import Request

from scrapers.manolo_scraper.spiders.spiders import ManoloBaseSpider
from ..errors import ParsingError
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from api.utils import make_hash


class EssaludSpider(ManoloBaseSpider):
    name = 'essalud'
    allowed_domains = ['visitas.essalud.gob.pe']
    NUMBER_OF_PAGES_PER_PAGE = 100_000
    DATE_REQUEST_FORMAT = '%d/%m/%Y'

    def initial_request(self, date):
        date_str = date.strftime(self.DATE_REQUEST_FORMAT)

        url = f'http://visitas.essalud.gob.pe/?reservation={date_str} - ' \
              f'{date_str}&search=&change_qti_page={self.NUMBER_OF_PAGES_PER_PAGE}'
        # This initial request always hit the current page of the date.
        request = Request(
            url=url,
            meta={'date': date_str},
            dont_filter=True,
            callback=self.parse,
        )
        return request

    def parse(self, response, **kwargs):
        date = self.get_date_item(response.meta['date'], self.DATE_REQUEST_FORMAT)
        rows = response.xpath('//tr[has-class("even")]')

        for row in rows:
            loader = ManoloItemLoader(item=ManoloItem(), selector=row)
            loader.add_value('institution', self.name)
            loader.add_value('date', date)
            loader.add_value('id_document', 'DNI')

            loader.add_xpath('full_name', './/td[3]/text()')

            id_number = row.xpath('.//td[4]/text()').extract_first(default='')
            if id_number:
                id_number = id_number.replace('DNI ', '')
            loader.add_value('id_number', id_number)

            loader.add_xpath('entity', './/td[5]/text()')
            loader.add_xpath('reason', './/td[6]/text()')
            loader.add_xpath('location', './/td[7]/text()')
            loader.add_xpath('host_name', './/td[8]/text()')
            loader.add_xpath('office', './/td[9]/text()')
            loader.add_xpath('meeting_place', './/td[10]/text()')

            loader.add_xpath('time_start', './/td[11]/text()')
            loader.add_xpath('time_end', './/td[12]/text()')

            time_start = loader.get_output_value('time_start')
            time_end = loader.get_output_value('time_end')

            loader.replace_value('time_start', self._get_time(time_start))
            loader.replace_value('time_end', self._get_time(time_end))

            item = loader.load_item()
            item = make_hash(item)

            yield item

    def _get_time(self, date_string):
        # date_string: '28/08/2015 05:11:38 p.m.'
        if date_string is None:
            return None

        if isinstance(date_string, str):
            return date_string
        elif isinstance(date_string, list) and len(date_string) > 0:
            return date_string[0]
        else:
            raise ParsingError(f'_get_time error: cannot parse {date_string}')
