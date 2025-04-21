import csv

from django.core.management.base import BaseCommand

from visitors.models import Visitor, Institution


class Command(BaseCommand):
    help = 'calculates the stats of visitors per institution'

    def handle(self, *args, **options):

        print("Doing calculations")
        run_statistics()


def run_statistics():
    all_stats = []
    institutions = Institution.objects.all()
    for institution in institutions:
        visitors = Visitor.objects.filter(institution2=institution).count()
        stats = {}
        stats['institution'] = institution.name
        stats['visitors'] = visitors
        all_stats.append(stats)

    with open("stats.csv", "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["visitors", "institution"])
        writer.writeheader()
        for item in all_stats:
            writer.writerow(item)
