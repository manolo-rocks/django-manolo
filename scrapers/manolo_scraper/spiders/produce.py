# -*- coding: utf-8 -*-
from .spiders import GobSpider


class ProduceSpider(GobSpider):
    name = 'produce'
    institution_name = 'produce'
    institution_ruc = '20504794637'
    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
