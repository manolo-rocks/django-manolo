import codecs
import config
from bs4 import BeautifulSoup
import os

def html_to_json(html):
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
            out  = i[0] + "|" + i[1] + "|" + i[2] + "|" + i[3] + "|"
            out += i[4] + "|" + i[5] + "|" + i[6] + "|" + i[7] + "|"
            out += i[8] + "|" + i[9] + "\n"
            f.write(out)
        else:
            print i
    f.close()


f = codecs.open("osce_page.html", "r", "utf8")
html = f.read()
f.close()

html_to_json(html)
