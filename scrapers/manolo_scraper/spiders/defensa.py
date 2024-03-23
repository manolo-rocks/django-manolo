import scrapy

from scrapers.manolo_scraper.spiders.spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash


class DefensaSpider(ManoloBaseSpider):
    name = 'defensa'
    allowed_domains = ['transparencia.gob.pe', '181.65.208.74']
    base_url = 'http://181.65.208.74/visitas/visitas_transparencia.php'

    def initial_request(self, date):
        # There is no pagination in Defensa
        date_str = date.strftime("%d/%m/%Y")
        params = {
            'fecha': date_str,
            'fecha2': date_str,
        }
        return scrapy.FormRequest(
            url=self.base_url,
            formdata=params,
            meta={'date': date_str},
            dont_filter=True,
            callback=self.parse,
        )

    def parse(self, response, **kwargs):
        rows = response.xpath('//tr')
        for idx, row in enumerate(rows):
            data = row.xpath('.//td[@class="clsgriddata2"]')

            if len(data) > 5:
                l = ManoloItemLoader(item=ManoloItem(), selector=row)

                l.add_value('institution', 'defensa')
                l.add_xpath('date', './/td[2]/text()')

                l.add_xpath('full_name', './/td[3]/text()')
                l.add_xpath('entity', './/td[5]/text()')
                l.add_xpath('reason', './/td[6]/text()')
                l.add_xpath('host_name', './/td[7]/text()')
                l.add_xpath('host_title', './/td[8]/text()')
                l.add_xpath('office', './/td[9]/text()')
                l.add_xpath('time_start', './/td[10]/text()')
                l.add_xpath('time_end', './/td[11]/text()')
                id_number = data[3].xpath('text()').extract_first(default='')
                l.add_value('id_document', 'DNI')
                l.add_value('id_number', id_number)

                item = l.load_item()
                item = make_hash(item)
                yield item
