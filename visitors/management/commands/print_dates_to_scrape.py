import csv
from copy import copy
from datetime import datetime, date, timedelta

from django.core.management import BaseCommand

from scrapers.manolo_scraper.pipelines import save_item
from scrapers.manolo_scraper.utils import get_dni, make_hash
from visitors.models import Visitor


class Command(BaseCommand):
    help = "Print dates that need scraping"

    def add_arguments(self, parser):
        parser.add_argument(
            '-i',
            '--institution',
            action='store',
            choices=[
                'pcm',
                'minjus',
                'minedu',
                'mincetur',
                'ambiente',
                'mef',
                'minagr',
                # to update,
                'minem',
                'vivienda',
                'min. mujer',
                'produce',
                'trabajo',
            ]
        )

    def handle(self, *args, **options):
        institution = options['institution']
        print_missing_dates(institution)


def print_missing_dates(institution):
    items = Visitor.objects.filter(
        institution=institution,
    ).distinct('date').values('date')

    all_dates = []
    for item in items:
        all_dates.append(item['date'])

    all_dates = sorted(all_dates)
    start_date = all_dates[0]

    now = date.today()
    diff = now - start_date

    for i in range(0, diff.days):
        day = start_date + timedelta(days=i)

        # it is a weekday 0 to 4
        if day not in all_dates \
                and day.weekday() < 5:
            print(day)
