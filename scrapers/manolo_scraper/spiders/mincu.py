# -*- coding: utf-8 -*-
from scrapers.manolo_scraper.spiders.spiders import GobSpider


class MincuSpider(GobSpider):
    name = 'mincu'
    institution_name = 'mincu'
    institution_ruc = '20537630222'
    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
