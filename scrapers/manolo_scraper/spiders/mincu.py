# -*- coding: utf-8 -*-
from scrapers.manolo_scraper.spiders.spiders import SireviSpider


class MincuSpider(SireviSpider):
    name = 'mincu'

    allowed_domains = ['visitas.cultura.gob.pe']

    base_url = 'http://visitas.cultura.gob.pe'

    institution_name = 'mincu'
