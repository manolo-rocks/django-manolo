# -*- coding: utf-8 -*-
from scrapers.manolo_scraper.spiders.spiders import GobSpider


class MTCSpider(GobSpider):
    name = 'mtc'
    institution_name = 'mtc'
    institution_ruc = '20131379944'

    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
