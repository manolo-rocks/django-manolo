"""Save scraped items into our database"""
import json

from django.core.management import BaseCommand

from scrapers.manolo_scraper.pipelines import process_item


class Command(BaseCommand):
    help = "Save manolo items in database"

    def add_arguments(self, parser):
        parser.add_argument('-i', '--input', action='store')

    def handle(self, *args, **options):
        input_file = options['input']
        save_items(input_file)


def save_items(input_file):
    print(f"processing {input_file}")

    with open(input_file) as handle:
        items = handle.readlines()

        for item in items:
            item = json.loads(item)
            process_item(item)
