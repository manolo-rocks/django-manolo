# -*- coding: utf-8 -*-

import requests
import codecs

def buscar(fecha):
    url = "http://visitas.osce.gob.pe/controlVisitas/index.php"
    url += "?r=consultas/visitaConsulta/index"

    payload = {
            "VisitaConsultaQueryForm[feConsulta]": fecha
            }
    r = requests.post(url, data=payload)
    return r.text.encode("utf-8")


fecha = "03/03/2014"
print buscar
