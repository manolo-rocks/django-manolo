import os
import time

from scrapy_splash import SplashRequest
import undetected_chromedriver.v2 as uc

from .spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import get_lua_script, make_hash


class MTCSpiderOld(ManoloBaseSpider):
    name = 'mtc_old'
    institution_name = 'mtc'
    base_url = 'http://scrv-reporte.mtc.gob.pe/'
    start_url = 'http://scrv-reporte.mtc.gob.pe/'
    allowed_domains = ['scrv-reporte.mtc.gob.pe']

    def initial_request(self, date):
        cwd = os.path.dirname(os.path.abspath(__file__))
        chromedriver_path = os.path.join(cwd, 'chromedriver')
        driver = uc.Chrome(executable_path=chromedriver_path, headless=True)

        driver.get(self.start_url)
        time.sleep(10)
        driver.save_screenshot('/tmp/datadome_undetected_webddriver.png')
        driver.close()

        date_str = date.strftime('%d/%m/%Y')
        print(date_str, get_lua_script('mtc.lua'))
        request = SplashRequest(
            url=self.base_url,
            # callback=self.parse,
            # endpoint='execute',
            # args={
            #     'lua_source': get_lua_script('mtc.lua'),
            #     'start_date': date_str,
            #     'end_date': date_str
            # },
            # meta={
            #     'date': date_str,
            # },
            dont_filter=True,
        )
        print(request)
        yield request

    def parse(self, response, **kwargs):
        with open("a.html", "w") as handle:
            handle.write(response.body)
        rows = response.xpath(
            '//table[@id="ctl00_ContentPlaceHolder_gdvReporteVisitasNuevo"]//tr[@class="gridRow"]'
        )
        date = self.get_date_item(response.meta.get('date'), '%d/%m/%Y')
        for row in rows:
            loader = ManoloItemLoader(item=ManoloItem(), selector=row)

            loader.add_value('date', date)
            loader.add_value('institution', 'mtc')
            loader.add_xpath('entity', './/td[@class="clsdetalle"][4]/text()')

            loader.add_xpath('reason', './td[9]/text()')
            loader.add_xpath('meeting_place', './td[8]/text()')
            loader.add_xpath('office', './td[1]/text()')
            loader.add_xpath('host_name', './td[3]/text()')
            loader.add_xpath('full_name', './td[7]/text()')
            loader.add_xpath('time_start', './td[4]/text()')
            loader.add_xpath('time_end', './td[5]/text()')

            loader.add_value('id_document', 'DNI')
            loader.add_xpath('id_number', './td[6]/text()')

            item = loader.load_item()
            item = make_hash(item)

            yield item
