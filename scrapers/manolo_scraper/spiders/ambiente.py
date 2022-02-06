# -*- coding: utf-8 -*-
from .spiders import GobSpider


class AmbienteSpider(GobSpider):
    name = 'ambiente'
    institution_name = 'ambiente'
    institution_ruc = '20492966658'

    start_url = f'https://visitas.servicios.gob.pe/consultas/index.php?ruc_enti={institution_ruc}'
