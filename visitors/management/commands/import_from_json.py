import json
from copy import copy
from datetime import datetime

from django.core.management import BaseCommand

from scrapers.manolo_scraper.pipelines import save_item
from scrapers.manolo_scraper.utils import get_dni, make_hash
from visitors.models import Visitor


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
            fecha = row['fecha']
            fecha = datetime.strptime(fecha, '%d/%m/%Y').date()
            id_document, id_number = get_dni(row['documento'])

            triad = [
                i.strip() for i in row['funcionario'].split('-')
            ]
            host_name = triad[0]
            office = " - ".join(triad[1:-1])
            host_title = triad[-1]

            lugar = row['no_lugar_r']

            item = {
                'institution': institution,
                'date': fecha,
                'full_name': row['visitante'],
                'entity': row['rz_empresa'],
                'reason': row['motivo'],
                'host_name': host_name,
                "time_start": row['horaIn'],
                "time_end": row['horaOut'],
                "id_number": id_number,
                "id_document": id_document,
                "office": office,
                "host_title": host_title,
                "meeting_place": lugar,
            }
            item = make_hash(item)
            save_item(item)
