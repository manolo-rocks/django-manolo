# -*- coding: utf-8 -*-
from scrapers.manolo_scraper.spiders.spiders import SireviSpider


class MinviSpiderOld(SireviSpider):
    name = 'minvi'

    allowed_domains = ['s01pweb001.vivienda.gob.pe']

    base_url = "http://s01pweb001.vivienda.gob.pe/Visitas/controlVisitas/index.php"

    institution_name = 'vivienda'
