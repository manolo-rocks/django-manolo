# -*- coding: utf-8 -*-
from scrapers.manolo_scraper.spiders.spiders import GobSpider


class MidisSpider(GobSpider):
    name = 'midis'
    institution_name = 'midis'
    institution_ruc = '20545565359'

    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
