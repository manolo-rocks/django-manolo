# -*- coding: utf-8 -*-
from scrapers.manolo_scraper.spiders.spiders import SireviSpider


class MinagrSpider(SireviSpider):
    name = 'minagr'

    allowed_domains = ['minagri.gob.pe']

    base_url = "https://visitas.minagri.gob.pe/visitas/controlVisitas/index.php?r=consultas/visitaConsulta/index"

    institution_name = 'minagr'
