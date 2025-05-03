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
        institution = input_file.split('/')[-1].replace(".json", "")
        save_items(input_file, institution)


def save_items(input_file, institution):
    print(f"processing {input_file} {institution}")

    with open(input_file) as handle:
        data = json.loads(handle.read())
        for row in data:
            process_row(row, institution)
