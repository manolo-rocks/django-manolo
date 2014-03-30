import codecs
import config
from bs4 import BeautifulSoup
import os

def html_to_json(html):
    import json

    # taken from http://stackoverflow.com/a/14167916
    soup = BeautifulSoup(html)
    table = soup.find('table', attrs={'class': 'items'})
    headers = [header.text for header in table.find_all('th')]

    rows = []
    for row in table.find_all('tr'):
        rows.append([val.text for val in row.find_all('td')])

    filename = os.path.join(config.base_folder, "output.json")
    f = codecs.open(filename, "a", "utf8")
    for i in rows:
        if len(i) > 1:
            out = dict()
            out['date'] = i[0].strip()
            out['visitor'] = i[1].strip()
            out['id_document'] = i[2].strip()
            out['entity'] = i[3].strip()
            out['objective'] = i[4].strip()
            out['host'] = i[5].strip()
            out['office'] = i[6].strip()
            out['meeting_place'] = i[7].strip()
            out['time_start'] = i[8].strip()
            try:
                out['time_end'] = i[9].strip()
            except:
                out['time_end'] = ""

            f.write(json.dumps(out) + "\n")
        else:
            print ""
    f.close()


f = codecs.open("osce_page.html", "r", "utf8")
html = f.read()
f.close()

html_to_json(html)
