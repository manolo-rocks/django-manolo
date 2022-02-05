# -*- coding: utf-8 -*-
from scrapers.manolo_scraper.spiders.spiders import GobSpider


class MineduSpider(GobSpider):
    name = 'minedu'
    institution_name = 'minedu'
    institution_ruc = '20131370998'
    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
