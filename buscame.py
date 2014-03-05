# -*- coding: utf-8 -*-

import requests
import csv
import os
import codecs
from bs4 import BeautifulSoup

def html_to_csv(html):
    # taken from http://stackoverflow.com/a/14167916
    soup = BeautifulSoup(html)
    table = soup.find('table', attrs={'class': 'items'})
    headers = [header.text.encode('utf8') for header in table.find_all('th')]

    rows = []
    for row in table.find_all('tr'):
        rows.append([val.text.encode('utf8') for val in row.find_all('td')])

    with open("output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(row for row in rows if row)

def buscar(fecha):
    url = "http://visitas.osce.gob.pe/controlVisitas/index.php"
    url += "?r=consultas/visitaConsulta/index"

    payload = {
            "VisitaConsultaQueryForm[feConsulta]": fecha
            }
    r = requests.post(url, data=payload)
    csv = html_to_csv(r.text)

    next_page = True
    while next_page == True:
        for i in range(2,50):
            url = "http://visitas.osce.gob.pe/controlVisitas/index.php"
            url += "?r=consultas/visitaConsulta/index"
            url += "&lstVisitasResult_page="
            url += str(i)
            print url
            try:
                r = requests.post(url, data=payload)
                csv = html_to_csv(r.text)
            except:
                next_page = False
                pass




# clean our outfile
try:
    os.remove("output.csv")
except OSError:
    pass

fecha = "05/03/2014"
buscar(fecha)
