# -*- coding: utf-8 -*-
import codecs
import datetime
from datetime import date
from datetime import timedelta as td
import hashlib
import json
from optparse import make_option
import os
from random import randint
import re
from time import sleep

from bs4 import BeautifulSoup
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from manolo.models import Manolo


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-u', '--url', action='store', dest='url',
                    help=u'Ingrese la dirección web del registro online.',
                    ),
    )
    args = 'URL'
    help = u'Ingrese la dirección web del registro online.'

    def __init__(self, *args, **options):
        super(Command, self).__init__(*args, **options)
        if hasattr(settings, 'CRAWLERA_USER') and settings.CRAWLERA_USER != "":
            self.CRAWLERA_USER = settings.CRAWLERA_USER
            self.CRAWLERA_PASS = settings.CRAWLERA_PASS
            self.proxies = {
                "http": "http://" + self.CRAWLERA_USER + ":" +
                        self.CRAWLERA_PASS + "@proxy.crawlera.com:8010/",
            }
            self.crawlera = True
            print("Using Crawlera as proxy.")
        else:
            self.crawlera = False

        # location for output.json containing scrapped data
        self.OUTPUT_JSON = os.path.join(settings.BASE_DIR, "output.json")
        self.USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Crazy Browser 1.0.5)",
            "curl/7.7.2 (powerpc-apple-darwin6.0) libcurl 7.7.2 (OpenSSL 0.9.6b)",
            "Mozilla/5.0 (X11; U; Linux amd64; en-US; rv:5.0) Gecko/20110619 Firefox/5.0",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b8pre) Gecko/20101213 Firefox/4.0b8pre",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; " "Trident/5.0) chromeframe/10.0.648.205",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)",
            "Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01",
            "Opera/9.80 (Windows NT 6.1; U; pl) Presto/2.7.62 Version/11.00",
            "Opera/9.80 (X11; Linux i686; U; pl) Presto/2.6.30 Version/10.61",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.861.0 Safari/535.2",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.812.0 Safari/535.1",
        ]

    def handle(self, *args, **options):
        user_url = options.get('url')

        # last date in database
        d1 = self.get_last_date_in_db()

        # remove output.json file
        if os.path.isfile(self.OUTPUT_JSON):
            os.remove(self.OUTPUT_JSON)

        # d1 = date(2014, 8, 15)
        # range to fetch
        d2 = d1 + td(days=8)
        delta = d2 - d1

        for i in range(delta.days + 1):
            my_date = d1 + td(days=i)
            my_date = my_date.strftime("%d/%m/%Y")
            self.search(my_date, user_url)

        # scrapped data has been written to a file as jsonlines
        self.stdout.write("Getting data from our json file")
        items = self.get_data()

        self.stdout.write("Uploading data from our json file")
        for i in items:
            try:
                Manolo.objects.get(sha512=i['sha512'])
            except Manolo.DoesNotExist:
                try:
                    i['date'] = datetime.datetime.strptime(
                        i['date'],
                        '%d/%m/%Y',
                    )
                except ValueError:
                    i['date'] = None
                m = Manolo(**i)
                m.save()

    def search(self, my_date, user_url):
        print("Searching for date: %s" % str(my_date))
        print("Requesting URL %s" % str(user_url))

        payload = {"VisitaConsultaQueryForm[feConsulta]": my_date}
        headers = {
            "User-Agent": self.USER_AGENTS[randint(0,
                                                   len(self.USER_AGENTS))-1],
        }

        if self.crawlera is True:
            r = requests.post(url=user_url, data=payload, headers=headers,
                              proxies=self.proxies,
                              )
        else:
            r = requests.post(url=user_url, data=payload, headers=headers)
        r.encoding = "utf8"

        # saving to file
        self.html_to_json(r.text)

        number_of_pages = self.get_number_of_page_results(r.text)

        if number_of_pages is not False:
            for i in range(2, int(number_of_pages)+1):
                url = user_url
                url += "&lstVisitasResult_page="
                url += str(i)
                try:
                    sleep(randint(5, 15))
                    if self.crawlera:
                        print("Requesting URL %s" % str(url))
                        r = requests.post(url=url, data=payload,
                                          headers=headers,
                                          proxies=self.proxies,
                                          )
                    else:
                        r = requests.post(url=url, data=payload,
                                          headers=headers,
                                          )
                    r.encoding = "utf8"
                    self.lib.html_to_json(r.text)
                except:
                    pass

    def html_to_json(self, html):
        # taken from http://stackoverflow.com/a/14167916
        soup = BeautifulSoup(html)
        table = soup.find('table', attrs={'class': 'items'})
        # headers = [header.text for header in table.find_all('th')]

        rows = []
        for row in table.find_all('tr'):
            rows.append([val.text for val in row.find_all('td')])

        filename = self.OUTPUT_JSON
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
        f.close()

    def get_number_of_page_results(self, html):
        soup = BeautifulSoup(html)
        res = soup.find_all(href=re.compile("lstVisitasResult_page=([0-9]+)"))
        pages = []
        for i in res:
            page = re.search("_page=([0-9]+)", str(i)).groups()[0]
            pages.append(int(page))
        pages = set(pages)
        if len(pages) > 0:
            pages = sorted(pages)[-1]
        else:
            pages = False
        return pages

    # upload scrapped data to our database
    def get_data(self):
        filename = self.OUTPUT_JSON
        f = codecs.open(filename, "r", "utf-8")
        data = f.readlines()
        f.close()

        items = []
        for line in data:
            line = line.strip()
            item = json.loads(line)

            if 'id_document' in item:
                id_doc_number = re.search("([0-9]+)", item['id_document'])
                if id_doc_number:
                    id_doc_number = id_doc_number.groups()[0]
                else:
                    id_doc_number = ""
            else:
                id_doc_number = ""

            string = str(item['date']) + str(id_doc_number)
            string += str(item['time_start'])
            m = hashlib.sha1()
            m.update(string)
            item['sha512'] = m.hexdigest()

            items.append(item)
        return items

    def get_last_date_in_db(self):
            l_date = Manolo.objects.exclude(date=None).order_by('date').last()
            if l_date:
                d1 = l_date.date - td(days=3)
            else:
                d1 = date(2011, 7, 28)
            return d1
