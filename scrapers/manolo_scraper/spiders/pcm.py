# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy import FormRequest
import undetected_chromedriver.v2 as uc

from .spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..utils import get_dni, make_hash

class PcmSpider(ManoloBaseSpider):
    name = 'pcm'
    institution_name = 'pcm'
    allowed_domains = ['visitas.servicios.gob.pe']
    base_url = 'https://visitas.servicios.gob.pe/consultas/dataBusqueda.php'

    def initial_request(self, date):
        """

            data = {
                'busqueda': '20168999926',
                'fecha': '27/08/2021+-+27/08/2021',
                }
        """
        import os
        cwd = os.path.dirname(os.path.abspath(__file__))
        chromedriver_path = os.path.join(cwd, 'chromedriver')
        driver = uc.Chrome(executable_path=chromedriver_path, headless=True)
        with driver:
            driver.get(self.base_url)
            html = driver.page_source
            with open('/tmp/gcaptcha.txt', 'w') as handle:
                handle.write(html)

        headers = {
            "Connection": "keep-alive",
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            'sec-ch-ua-mobile': '?0',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://visitas.servicios.gob.pe",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti=20168999926",
            "Accept-Language": "en-US,en;q=0.5",
        }
        date_str = date.strftime("%d/%m/%Y")
        data = {
            'busqueda': '20168999926',
            'fecha': f'{date_str} - {date_str}',
            'token': '03AGdBq27MI733wCC_kmdcVc3furrlmKe54-5t8CCcoj4r0WJT_y8cCdpaWRuJ-30gQRytxxVLtQ-gLb2pQ-etuKlCy1C7ciejmntcj-Ccswwod6ZW2qbLRldmJDwe92B6RGckoEjy-pE6-CGy_LOYx1e42_k65_jHVeEF1-BaR1_ok2-gb80pQzUf1h-qy6zKNkVZMUW9SRJ1Ic23MinRwbAHoL5J97x2H6lKJDifld1jbX0-TYkdqh9XaAThU3dXu2krmYfqFIrq35KQgniEq1WD5LNUovogwpUWiCeNs5v-5aP7qFQVLKE0WgZX1hzd9F1EBVLGEYgotg1d3GDyP4l7ZTUWnsVSDTaXAuJZfbFjtrCmFhn4Uo6xl-ZaMCcS-ZyDzjpkWJ1ViAKjUZraGSaY_xR8yGuNix1Cn30VHxRrTvx7V8ghJadTHwliHlRGIAr_uV1p7y2PwfTUxwNOoYDIK6jLhzytlw',
        }
        print(urllib.parse.urlencode(data))
        request = scrapy.Request(
            url=self.base_url,
            body=urllib.parse.urlencode(data),
            method='POST',
            headers=headers,
            meta={'date': date_str},
            callback=self.parse,
        )
        return request

    def parse(self, response, **kwargs):
        print(response.text)
        date_str = response.meta['date']
        visitors = response.json().get('data', [])

        for item in visitors:
            yield self.get_item(item, date_str)

    def get_item(self, item, date_str):
        funcionario_triad = [i.strip() for i in item['funcionario'].split('-')]
        try:
            host_name = funcionario_triad[0]
        except IndexError:
            host_name = ''

        try:
            office = funcionario_triad[1]
        except IndexError:
            office = ''

        try:
            host_title = funcionario_triad[2]
        except IndexError:
            host_title = ''

        l = ManoloItem(
            institution=self.institution_name,
            date=date_str,
            full_name=item['visitante'],
            entity=item['rz_empresa'],
            reason=item['motivo'],
            office=office,
            meeting_place=item['no_lugar_r'],
            host_name=host_name,
            host_title=host_title,
            time_start=item['horaIn'],
            time_end=item['horaOut'],
        )
        l = make_hash(l)
        return l
