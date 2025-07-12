# your_app/management/commands/generate_sitemaps.py
import logging

import requests
from django.core.management.base import BaseCommand
from django.conf import settings

from visitors.models import Visitor

log = logging.getLogger(__name__)

"""
POST /IndexNow HTTP/1.1
                    Content-Type: application/json; charset=utf-8
                    Host: api.indexnow.org
                    {
                      "host": "www.example.org",
                      "key": "dc0256884e6b414bb8be5f3e51b93b1f",
                      "keyLocation": "https://www.example.org/dc0256884e6b414bb8be5f3e51b93b1f.txt",
                      "urlList": [
                          "https://www.example.org/url1",
                          "https://www.example.org/folder/url2",
                          "https://www.example.org/url3"
                          ]
                    }
"""


class Command(BaseCommand):
    help = 'Submit sitemaps to IndexNow'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size', type=int, default=10_000,
            help='Number of URLs per sitemap file (max 50000)'
        )
        parser.add_argument(
            '--total', type=int, default=None,
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        self.stdout.write(f"Generating sitemaps with {batch_size} URLs per file...")

        total_to_do = options['total']

        # Count total DNIs
        self.total_dnis = Visitor.objects.values('id_number').distinct().count()
        self.count = 0

        for i in range(self.total_dnis):
            offset = i * batch_size
            dnis = Visitor.objects.values_list(
                'id_number', flat=True
            ).distinct().order_by('id_number')[offset:offset + batch_size]
            urls = []
            for dni in dnis:
                if not dni:
                    continue
                urls.append(f'https://manolo.rocks/visitas/{dni}/')
            self.post_dni_pages(urls)
            if total_to_do and self.count >= total_to_do:
                break

    def post_dni_pages(self, urls):
        self.count += len(urls)
        url = 'https://api.indexnow.org/indexnow'
        data = {
            "host": "manolo.rocks",
            "key": settings.INDEXNOW_KEY,
            "keyLocation": f"https://manolo.rocks/{settings.INDEXNOW_KEY}.txt",
            "urlList": urls
        }
        print(f"Posting {self.count}/{self.total_dnis}")
        res = requests.post(
            url,
            json=data,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Host": "api.indexnow.org"
            }
        )
        print(res.status_code, res.text)
