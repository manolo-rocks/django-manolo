# -*- coding: utf-8 -*-
from scrapers.manolo_scraper.spiders.spiders import SireviSpider


class MineduSpider(SireviSpider):
    name = 'minedu'

    allowed_domains = ['visitasmed.perueduca.edu.pe']

    base_url = 'http://visitasmed.perueduca.edu.pe/controlVisitas'

    institution_name = 'minedu'
