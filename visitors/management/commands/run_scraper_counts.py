from django.core.management.base import BaseCommand
from django.utils import timezone

from visitors.models import Visitor, Statistic, Institution, VisitorScrapeProgress


class Command(BaseCommand):
    help = 'computes the total number of records in visitors and last updated per scraper'

    def handle(self, *args, **options):

        print("Doing calculations")
        run_counts()


def run_counts():
    store_total_visitor_count()
    store_updated_institutions()


def store_total_visitor_count():
    stats = Statistic.objects.all().last()
    stats.visitor_count = Visitor.objects.all().count()
    stats.save()
    print(f'Total count {stats.visitor_count}')

    if not VisitorScrapeProgress.objects.filter(cutoff_date=timezone.now()).exists():
        VisitorScrapeProgress.objects.create(
            visitor_count=stats.visitor_count,
            cutoff_date=timezone.now(),
        )

    return stats


def store_updated_institutions():
    stats = Statistic.objects.all().last()

    institution_stats = []

    for institution in Institution.objects.all().order_by('-rank'):
        last_visitor = Visitor.objects.filter(
            institution=institution.slug,
        ).order_by('modified').last()
        last_updated = timezone.localtime(last_visitor.modified)

        if last_visitor:
            item = {
                'name': institution.name,
                'slug': institution.slug,
                'rank': institution.rank,
                'last_updated': last_updated.strftime('%Y-%m-%d %H:%M:%S'),
            }
            institution_stats.append(item)
            print(f'{institution} last updated {item["last_updated"]}')

    stats.updated_institutions = institution_stats
    stats.save()
