import json

from scrapy import FormRequest

from scrapers.manolo_scraper.spiders.spiders import ManoloBaseSpider
from ..item_loaders import ManoloItemLoader
from ..items import ManoloItem
from ..utils import make_hash, get_dni


class INPESpider(ManoloBaseSpider):
    name = 'inpe'
    allowed_domains = [
        'apps.inpe.gob.pe',
    ]

    def initial_request(self, date):
        date_str = date.strftime('%d/%m/%Y')
        url = f'https://apps.inpe.gob.pe/VisitasadmInpe/CargarTablaVisitaJSON?FechaVisita={date_str}&local=-1'  # noqa
        requests = FormRequest(
            url,
            meta={'date': date_str},
            dont_filter=True,
            callback=self.parse,
        )
        return requests

    def parse(self, response, **kwargs):
        data = json.loads(response.text)['aaData']
        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        for row in data:
            loader = ManoloItemLoader(item=ManoloItem(), selector=row)

            loader.add_value('institution', 'inpe')
            loader.add_value('date', date)

            loader.add_value('full_name', row[1])

            dni_str, dni_number = get_dni(row[2])
            loader.add_value('id_document', dni_str)
            loader.add_value('id_number', dni_number)
            loader.add_value('entity', row[3])
            loader.add_value('time_start', row[4])
            loader.add_value('time_end', row[5])
            loader.add_value('reason', row[6])
            loader.add_value('host_name', row[7])
            loader.add_value('host_title', row[8])
            loader.add_value('office', row[9])
            loader.add_value('location', row[10])
            item = loader.load_item()
            item = make_hash(item)
            yield item
