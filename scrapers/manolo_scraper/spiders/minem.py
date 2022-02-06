# -*- coding: utf-8 -*-
from .spiders import GobSpider


class MinemSpider(GobSpider):
    name = 'minem'
    institution_name = 'minem'
    institution_ruc = '20131368829'
    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
