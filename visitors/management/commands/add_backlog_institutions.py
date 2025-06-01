import csv

from django.core.management import BaseCommand

from visitors.models import Institution


class Command(BaseCommand):
    help = "Add list of institutions that need scraping"

    def add_arguments(self, parser):
        parser.add_argument('-f', '--filename', action='store')

    def handle(self, *args, **options):
        input_file = options['filename']
        with open(input_file) as f:
            reader = csv.reader(f)

            for row in reader:
                name, ruc, slug = row
                try:
                    Institution.objects.get(ruc=ruc)
                except Institution.DoesNotExist:
                    Institution.objects.create(
                        name=name,
                        ruc=ruc,
                        slug=slug
                    )
                    print((ruc, slug))
