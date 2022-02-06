# -*- coding: utf-8 -*-
from .spiders import GobSpider


class MujerSpider(GobSpider):
    name = 'mujer'
    institution_name = 'min. mujer'
    institution_ruc = '20336951527'
    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
