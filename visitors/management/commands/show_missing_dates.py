"""For a given institution search missing dates to scrape"""
from datetime import date

from django.core.management import BaseCommand
from django.utils import timezone

from visitors.models import Visitor


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-i', '--institution', action='store')

    def handle(self, *args, **options):
        institution = options['institution']
        search_missing_dates(institution)


def search_missing_dates(institution):
    print(f"searching for {institution}")
    scraped_dates = set()
    visits = Visitor.objects.filter(institution=institution)

    for visit in visits.iterator(chunk_size=100):
        scraped_dates.add(visit.date)

    start = scraped_dates[0]
    start_year = start.year
    years = list(range(start_year, timezone.now().year + 1))
    months = list(range(1, 13))
    days = list(range(1, 32))

    missing_dates = list()

    for year in years:
        for month in months:
            for day in days:
                try:
                    current_date = date(year, month, day)
                except ValueError:
                    continue

                if current_date not in scraped_dates:
                    missing_dates.append(current_date)



