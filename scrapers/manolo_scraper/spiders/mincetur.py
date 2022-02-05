# -*- coding: utf-8 -*-
from .spiders import GobSpider


class MinceturSpider(GobSpider):
    name = 'mincetur'
    institution_name = 'mincetur'
    institution_ruc = '20504774288'

    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
