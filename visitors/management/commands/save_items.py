"""Save scraped items into our database"""
import json

from django.core.management import BaseCommand

from scrapers.manolo_scraper.pipelines import process_item


"""
saving from cron jobs does not work

# */10 11-23 * * * cd /code && /usr/local/bin/python manage.py run_scraper_counts 2>> /tmp/scraper_counts.log
# */10 1-10 * * * cd /code && /usr/local/bin/python manage.py run_scraper_counts 2>> /tmp/scraper_counts.log

# */5 11-23 * * * cd /code && /usr/local/bin/python manage.py save_items -i /tmp/pcm.jl 2>> /tmp/saving_err_pcm.log > /tmp/saving_pcm.log
# */5 1-10 * * * cd /code && /usr/local/bin/python manage.py save_items -i /tmp/pcm.jl 2>> /tmp/saving_err_pcm.log > /tmp/saving_pcm.log

# */6 11-23 * * * cd /code && /usr/local/bin/python manage.py save_items -i /tmp/congreso.jl 2>> /tmp/saving_err_congreso.log > /tmp/saving_congreso.log
# */6 1-10 * * * cd /code && /usr/local/bin/python manage.py save_items -i /tmp/congreso.jl 2>> /tmp/saving_err_congreso.log > /tmp/saving_congreso.log

# */7 11-23 * * * cd /code && /usr/local/bin/python manage.py save_items -i /tmp/presidencia.jl 2>> /tmp/saving_err_presidencia.log > /tmp/saving_presidencia.log
# */7 1-10 * * * cd /code && /usr/local/bin/python manage.py save_items -i /tmp/presidencia.jl 2>> /tmp/saving_err_presidencia.log > /tmp/saving_presidencia.log
"""

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
