# -*- coding: utf-8 -*-
from scrapers.manolo_scraper.spiders.spiders import GobSpider


class JusticiaSpider(GobSpider):
    name = 'justicia'
    institution_name = 'minjus'
    institution_ruc = '20131371617'
    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
