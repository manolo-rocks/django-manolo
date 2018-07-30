import csv

from django.core.management.base import BaseCommand

from visitors.models import Visitor
from visitors.management.commands.import_perucompras import get_visit_date_str, \
    get_time_start, get_time_end, make_hash


class Command(BaseCommand):
    help = 'update records in the database, add date to perucompras records'

    def add_arguments(self, parser):
        parser.add_argument("filename")

    def handle(self, *args, **options):
        do_update(options["filename"])


def do_update(filename):
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date_str = get_visit_date_str(row)
            time_start = get_time_start(row)
            time_end = get_time_end(row)

            item = {
                "institution": "perucompras",
                "full_name": row["nombre_visita"],
                "id_document": "dni",
                "id_number": row["documento"],
                "date": date_str,
                "time_start": time_start,
                "time_end": time_end,
            }
            item = make_hash(item)
            hash_str = item["sha1"]
            record = Visitor.objects.get(sha1=hash_str)
            if not record:
                print("error, cannot find in db ", row)
            else:
                record.date = date_str
                record.save()
