# -*- coding: utf-8 -*-
from .spiders import GobSpider


class MinagrSpider(GobSpider):
    name = 'minagr'
    institution_name = 'minagr'
    institution_ruc = '20131372931'
    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
