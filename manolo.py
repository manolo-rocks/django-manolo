# -*- coding: utf8 -*-

import dataset
import requests
import config
import csv
import lib
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
    headers = [header.text for header in table.find_all('th')]

    rows = []
    for row in table.find_all('tr'):
        rows.append([val.text for val in row.find_all('td')])

    filename = os.path.join(config.base_folder, "output.csv")
    f = codecs.open(filename, "a", "utf8")
    for i in rows:
        if len(i) > 1:
            out  = i[0] + "," + i[1] + "," + i[2] + "," + i[3] + ","
            out += i[4] + "," + i[5] + "," + i[6] + "," + i[7] + ","
            out += i[8] + "," + i[9] + "\n"
            f.write(out)
        else:
            print i
    f.close()

    #with codecs.open("output.csv", "a", "utf8") as f:
        #writer = csv.writer(f)
        #writer.writerow(headers)
        #writer.writerows(row for row in rows if row)

def get_number_of_page_results(html):
    soup = BeautifulSoup(html)
    res = soup.find_all(href=re.compile("lstVisitasResult_page=([0-9]+)"))
    pages = []
    for i in res:
        page = re.search("_page=([0-9]+)", str(i)).groups()[0]
        pages.append(page)
    pages = set(pages)
    print pages
    if len(pages) > 0:
        pages = sorted(pages)[-1]
    else:
        pages = False
    return pages


def buscar(fecha):
    url = "http://visitas.osce.gob.pe/controlVisitas/index.php"
    url += "?r=consultas/visitaConsulta/index"

    payload = {
            "VisitaConsultaQueryForm[feConsulta]": fecha
            }
    r = requests.post(url, data=payload)
    r.encoding = "utf8"
    csv = html_to_csv(r.text)
    print url

    number_of_pages = get_number_of_page_results(r.text)

    if number_of_pages != False:
        for i in range(2, int(number_of_pages)+1):
            url = "http://visitas.osce.gob.pe/controlVisitas/index.php"
            url += "?r=consultas/visitaConsulta/index"
            url += "&lstVisitasResult_page="
            url += str(i)
            print url
            try:
                r = requests.post(url, data=payload)
                r.encoding = "utf8"
                csv = html_to_csv(r.text)
            except:
                pass

def last_date_in_db():
    lib.create_database()
    filename = os.path.join(config.base_folder, "visitas.db")
    db = dataset.connect("sqlite:///" + filename)
    res = db.query("select date from visitas")

    dates = []
    for i in res:
        i = i['date'].split("/")
        dates.append(date(int(i[2]), int(i[1]), int(i[0])))
    dates.sort()
    return dates[-1]




# clean our outfile
try:
    filename = os.path.join(config.base_folder, "output.csv")
    os.remove(filename)
except OSError:
    pass

# Use this format for dates
# fecha = "DD/MM/YYYY"

# Days between two dates
# taken from http://stackoverflow.com/a/7274316
#d1 = date(2012,12,1)
#d2 = date(2014,3,7)
d1 = last_date_in_db() - td(days=3)
d2 = d1 + td(days=6)
delta = d2 - d1
for i in range(delta.days + 1):
    my_date = d1 + td(days=i)
    fecha = my_date.strftime("%d/%m/%Y")
    print fecha

    buscar(fecha)


# upload data from our csv file
items = lib.get_data()
filename = os.path.join(config.base_folder, "visitas.db")
db = dataset.connect("sqlite:///" + filename)
table = db['visitas']

for i in items:
    if not table.find_one(sha512=i['sha512']):
        print i['sha512'], i['date']
        table.insert(i)

lib.recreate_website()
