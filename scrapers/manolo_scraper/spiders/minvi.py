# -*- coding: utf-8 -*-
from scrapers.manolo_scraper.spiders.spiders import GobSpider


class MinviSpider(GobSpider):
    name = 'minvi'
    institution_name = 'vivienda'
    institution_ruc = '20504743307'
    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
