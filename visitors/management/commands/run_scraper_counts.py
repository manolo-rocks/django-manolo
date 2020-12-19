import math

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from twitterbot.bot import TwitterBot

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

    last_entry = VisitorScrapeProgress.objects.last()

    if last_entry:
        last_entry_millions = math.floor(last_entry.visitor_count / 1_000_000)
        current_count_millions = math.floor(stats.visitor_count / 1_000_000)
        if current_count_millions - last_entry_millions > 0:
            twitter = TwitterBot(
                settings.TWITTER_CONSUMER_KEY,
                settings.TWITTER_CONSUMER_SECRET,
                settings.TWITTER_OAUTH_TOKEN,
                settings.TWITTER_OAUTH_TOKEN_SECRET,
            )
            twitter.send_tweet(
                f'la base de datos de manolo.rocks sobrepasó los {current_count_millions} millones '
                f'de registros de visitas con {stats.visitor_count:,} registros'
            )

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
        ).order_by('date').last()

        if last_visitor:
            item = {
                'name': institution.name,
                'slug': institution.slug,
                'rank': institution.rank,
                'last_updated': last_visitor.date.strftime('%Y-%m-%d'),
            }
            institution_stats.append(item)
            print(f'{institution} last updated {item["last_updated"]}')

    stats.updated_institutions = institution_stats
    stats.save()
