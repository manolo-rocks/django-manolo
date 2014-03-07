#!/usr/bin/python
# -*- coding: utf8 -*-

import json
import cgi
import cgitb
import dataset
import lib
import sys
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
    return s

if 'q' in data:
    q = sanitize(data['q'].value)

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
    out = "<table class='table table-hover table-striped table-bordered table-responsive table-condensed' "
    out += " style='font-size: 12px;'>"
    out += "<th>Fecha</th><th>Visitante</th><th>Documento</th><th>Entidad</th>"
    out += u"<th>Motivo</th><th>Empleado público</th><th>Oficina/Cargo</th>"
    out += u"<th>Lugar de reunión</th><th>Hora ing.</th><th>Hora sal.</th>\n"
    for i in res:
        out += lib.prettify(i)
    out += "\n</table>"

    f = codecs.open("base.html", "r", "utf8")
    html = f.read()
    f.close()

    out = html.replace("{% content %}", out)

    print "Content-Type: text/html\n"
    print out.encode("utf8")
else:
    pass
