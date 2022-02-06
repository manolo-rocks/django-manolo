# -*- coding: utf-8 -*-
from .spiders import GobSpider


class MefSpider(GobSpider):
    name = 'mef'
    institution_name = 'mef'
    institution_ruc = '20131370645'

    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
