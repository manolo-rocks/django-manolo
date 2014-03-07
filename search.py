#!/usr/bin/python
# -*- coding: utf8 -*-

import json
import cgi
import cgitb
import dataset
import lib
import sys
import re
import codecs
import string
import config
cgitb.enable()

data = cgi.FieldStorage()


def sanitize(s):
    s = s.replace("'", "")
    s = s.replace("-", "")
    s = s.replace('"', "")
    s = s.replace("\\", "")
    s = s.replace(";", "")
    s = s.replace("=", "")
    s = s.replace("*", "")
    s = s.replace("%", "")
    try:
        res = re.search("([0-9]{2,}/[0-9]{2,}/[0-9]{4,})", s)
        if res:
            s = res.groups()[0]
    except:
        s = ""
    return s


message = u"""<p>Este es <b>Manolo</b>. Un buscador de personas que visitan las instalaciones del
            Organismo Supervisor de las Contrataciones del Estado.
            <br />
            Todos los datos son descargados diariamente de aquí: <b><a href="http://visitas.osce.gob.pe/controlVisitas/index.php?r=consultas/visitaConsulta/index">
            http://visitas.osce.gob.pe/controlVisitas/index.php?r=consultas/visitaConsulta/index</a></b>
            </p>
            <p>
            Puedes buscar por nombre o palabra clave. 
            También puedes hacer búsquedas haciendo click sobre cada uno de los resultados.
            </p>
            """

if 'q' in data:
    q = sanitize(data['q'].value)

    if q != "":
        db = dataset.connect("sqlite:///visitas.db")
        # We will limit to show only 20 results per page
        query = "SELECT * FROM visitas WHERE "
        query += " date like '%" + q + "%' OR"
        query += " visitor like '%" + q + "%' OR"
        query += " id_document like '%" + q + "%' OR"
        query += " entity like '%" + q + "%' OR"
        query += " objective like '%" + q + "%' OR"
        query += " host like '%" + q + "%' OR"
        query += " office like '%" + q + "%' OR"
        query += " meeting_place like '%" + q + "%' "
        query += " limit 100 "
        res = db.query(query)
        out = u"<p>También puedes hacer búsquedas haciendo click sobre cada uno de los resultados.</p>"
        out += "<table class='table table-hover table-striped table-bordered table-responsive table-condensed' "
        out += " style='font-size: 12px;'>"
        out += "<th>Fecha</th><th>Visitante</th><th>Documento</th><th>Entidad</th>"
        out += u"<th>Motivo</th><th>Empleado público</th><th>Oficina/Cargo</th>"
        out += u"<th>Lugar de reunión</th><th>Hora ing.</th><th>Hora sal.</th>\n"
        j = 0
        for i in res:
            out += lib.prettify(i)
            j += 1
        out += "\n</table>"

        if j < 1:
            out = False

    f = codecs.open("base.html", "r", "utf8")
    html = f.read()
    f.close()

    if out:
        out = html.replace("{% content %}", out)
        out = out.replace("{% intro_message %}", "")
        out = out.replace("{% base_url %}", config.base_url)
        out = out.replace("{% keyword %}", q.decode("utf-8"))
    else:
        out = html.replace("{% intro_message %}", message)
        out = out.replace("{% content %}", "")
        out = out.replace("{% base_url %}", config.base_url)
        out = out.replace("{% keyword %}", q.decode("utf-8"))

    print "Content-Type: text/html\n"
    print out.encode("utf8")
else:
    f = codecs.open("base.html", "r", "utf8")
    html = f.read()
    f.close()

    out = html.replace("{% intro_message %}", message)
    out = out.replace("{% content %}", "")
    out = out.replace("{% base_url %}", config.base_url)

    print "Content-Type: text/html\n"
    print out.encode("utf8")
