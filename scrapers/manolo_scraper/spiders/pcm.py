# -*- coding: utf-8 -*-
from .spiders import GobSpider


class PcmSpider(GobSpider):
    name = 'pcm'
    institution_name = 'pcm'
    institution_ruc = '20168999926'
    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
