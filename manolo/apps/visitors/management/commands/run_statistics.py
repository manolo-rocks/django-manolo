from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from visitors.models import Visitor, Statistic


class Command(BaseCommand):
    help = 'calculates the five people that visited the most'
    
    def handle(self, *args, **options):

        print("Doing calculations")
        run_statistics()


def run_statistics():
    all_visitor_names = Visitor.objects.all().values_list(
        "full_name", flat=True,
    )
    all_visitor_names_unique = set(all_visitor_names)
    print(len(all_visitor_names_unique))

    visitors = Visitor.objects.all().values_list(
        "full_name",
    ).annotate(
        the_count=Count("full_name"),
    ).order_by(
        '-the_count',
    )[:100]
    Statistic.objects.all().delete()
    for visitor in visitors:
        Statistic.objects.create(full_name=visitor[0], number_of_visits=visitor[1])
        



