from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from visitors.models import Visitor, Statistic


class Command(BaseCommand):
    help = 'calculates the five people that visited the most'
    
    def handle(self, *args, **options):

        print("Doing calculations")
        run_statistics()


def run_statistics():
    visitors = Visitor.objects.all().values_list(
        "full_name",
    ).annotate(
        the_count=Count("full_name"),
    ).order_by(
        '-the_count',
    )[:5]
    for visitor in visitors:
        Statistic.objects.create(full_name=visitor[0], number_of_visits=visitor[1])



