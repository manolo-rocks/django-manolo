# -*- coding: utf-8 -*-

import requests
import csv
import re
import sys
import os
import codecs
from bs4 import BeautifulSoup
from datetime import date, timedelta as td

def html_to_csv(html):
    # taken from http://stackoverflow.com/a/14167916
    soup = BeautifulSoup(html)
    table = soup.find('table', attrs={'class': 'items'})
    headers = [header.text.encode('utf8') for header in table.find_all('th')]

    rows = []
    for row in table.find_all('tr'):
        rows.append([val.text.encode('utf8') for val in row.find_all('td')])

    with open("output.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(row for row in rows if row)

def get_number_of_page_results(html):
    soup = BeautifulSoup(html)
    res = soup.find_all(href=re.compile("lstVisitasResult_page=([0-9]+)"))
    pages = []
    for i in res:
        page = re.search("_page=([0-9]+)", str(i)).groups()[0]
        pages.append(page)
    pages = set(pages)
    pages = sorted(pages)
    return pages


def buscar(fecha):
    url = "http://visitas.osce.gob.pe/controlVisitas/index.php"
    url += "?r=consultas/visitaConsulta/index"

    payload = {
            "VisitaConsultaQueryForm[feConsulta]": fecha
            }
    r = requests.post(url, data=payload)
    csv = html_to_csv(r.text)

    number_of_pages = get_number_of_page_results(r.text)

    for i in number_of_pages:
        url = "http://visitas.osce.gob.pe/controlVisitas/index.php"
        url += "?r=consultas/visitaConsulta/index"
        url += "&lstVisitasResult_page="
        url += str(i)
        print url
        try:
            r = requests.post(url, data=payload)
            csv = html_to_csv(r.text)
        except:
            pass




# clean our outfile
try:
    os.remove("output.csv")
except OSError:
    pass

# Use this format for dates
# fecha = "DD/MM/YYYY"

# Days between two dates
# taken from http://stackoverflow.com/a/7274316
d1 = date(2011,7,28)
d2 = date(2014,3,8)
delta = d2 - d1
for i in range(delta.days + 1):
    my_date = d1 + td(days=i)

#buscar(fecha)
