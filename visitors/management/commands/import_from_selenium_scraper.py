import json

from django.core.management import BaseCommand

from api.utils import process_row


class Command(BaseCommand):
    help = "Save items downloaded as JSON. Update them if the are missing DNI"

    def add_arguments(self, parser):
        """
        Institution is inferred from filename
                'pcm',
                'minjus',
                'minedu',
                'mincetur',
                'ambiente',
                'mef',
                'minagr',
                'minem',
                'vivienda',
                'min. mujer',
                'produce',
                'trabajo',
        """
        parser.add_argument('-f', '--filename', action='store')

    def handle(self, *args, **options):
        input_file = options['filename']
        save_items(input_file)


def save_items(input_file):
    print(f"processing {input_file}")

    with open(input_file) as handle:
        lines = handle.readlines()
        for row in lines:
            row = json.loads(row)
            process_row(row)
