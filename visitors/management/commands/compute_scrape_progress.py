"""Keep track of number of visitors kept in our db per date

Keep stats 1 per month or when we reach milestones:
- 0
- 10k
- 100k
- 1 million
- then every 1 million
"""
from datetime import datetime

from django.core.management import BaseCommand

from visitors.models import Visitor, VisitorScrapeProgress


class Command(BaseCommand):
    help = __doc__

    def handle(self, *args, **options):
        process()


def process():
    date_start = Visitor.objects.all().order_by('created').first().created
    date_end = Visitor.objects.all().order_by('created').last().created

    for year in range(date_start.year, date_end.year + 1):
        for month in range(1, 13):
            cut_off = datetime(year, month, 1)
            recorded_count = VisitorScrapeProgress.objects.filter(
                cutoff_date=cut_off.date()
            )
            if recorded_count.exists():
                print(f'skipping {cut_off}')
                continue

            count = Visitor.objects.filter(created__lte=cut_off).count()
            if not count:
                continue
            VisitorScrapeProgress.objects.create(
                visitor_count=count,
                cutoff_date=cut_off
            )
            print(f'created {cut_off} for {count} Visitors')
