# -*- coding: utf-8 -*-
from scrapers.manolo_scraper.spiders.spiders import GobSpider


class TrabajoSpider(GobSpider):
    name = 'trabajo'
    institution_name = 'trabajo'
    institution_ruc = '20131023414'
    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
