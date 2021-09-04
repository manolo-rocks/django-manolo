# -*- coding: utf-8 -*-
import time
import urllib
import os

import scrapy
import undetected_chromedriver.v2 as uc

from .spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..utils import make_hash


class MefSpider(ManoloBaseSpider):
    name = 'mef'
    institution_name = 'mef'
    institution_ruc = '20131370645'
    allowed_domains = ['visitas.servicios.gob.pe']
    base_url = 'https://visitas.servicios.gob.pe/consultas/dataBusqueda.php'
    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'

    def initial_request(self, date):
        """
        Bypass google recaptcha.
        The government page does a request to google's recaptcha when user clicks
        the button to search for visit records.
        Google returns a token and a score that tells if request comes from human
        or bot.
        The government page uses the score to allow users to see results.

        We bypass by doing the request to google's recaptcha ourselves using
        selenium and getting the token.
        Use the token to make requests directly to their API.

            data = {
                'busqueda': '20168999926',
                'fecha': '27/08/2021+-+27/08/2021',
                'token': 'ble',
                }
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        chromedriver_path = os.path.join(cwd, 'chromedriver')
        driver = uc.Chrome(executable_path=chromedriver_path, headless=True)

        driver.get(self.start_url)
        time.sleep(10)
        token = driver.execute_script(
            "return grecaptcha.execute('6LdKTSocAAAAAN_TWX3cgpUMgIKpw_zGrellc3Lj', {action: 'create_comment'})"
        )
        time.sleep(6)

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
            'busqueda': self.institution_ruc,
            'fecha': f'{date_str} - {date_str}',
            'token': token,
        }
        request = scrapy.Request(
            url=self.base_url,
            body=urllib.parse.urlencode(data),
            method='POST',
            headers=headers,
            meta={'date': date_str},
            callback=self.parse,
        )
        driver.close()
        return request

    def parse(self, response, **kwargs):
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

        full_name = item.get('visitante', '') or ''
        entity = item.get('rz_empresa', '') or ''
        reason = item.get('motivo', '') or ''
        meeting_place = item.get('no_lugar_r', '') or ''
        time_start = item.get('horaIn', '') or ''
        time_end = item.get('horaOut', '') or ''

        l = ManoloItem(
            institution=self.institution_name,
            date=date_str,
            full_name=full_name.strip(),
            entity=entity.strip(),
            reason=reason.strip(),
            office=office,
            meeting_place=meeting_place.strip(),
            host_name=host_name,
            host_title=host_title,
            time_start=time_start.strip(),
            time_end=time_end.strip(),
        )
        l = make_hash(l)
        return l
