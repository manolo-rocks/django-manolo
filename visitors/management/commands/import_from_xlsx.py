import csv
from copy import copy
from datetime import datetime

from django.core.management import BaseCommand
import pandas as pd

from scrapers.manolo_scraper.pipelines import save_item
from scrapers.manolo_scraper.utils import get_dni, make_hash
from visitors.models import Visitor


class Command(BaseCommand):
    help = "Save items downloaded as XLSX. Update them if the are missing DNI"

    def add_arguments(self, parser):
        parser.add_argument('-f', '--filename', action='store')
        parser.add_argument(
            '-i',
            '--institution',
            action='store',
            choices=[
                'pcm',
                'minjus',
                'minedu',
                'mincetur',
                'ambiente',
                'mef',
                'minagr',
                # to update,
                'minem',
                'vivienda',
                'min. mujer',
                'produce',
                'trabajo',
            ]
        )

    def handle(self, *args, **options):
        input_file = options['filename']
        institution = options['institution']
        csv_file_name = convert_to_csv(input_file)
        save_items(csv_file_name, institution)


def convert_to_csv(input_file) -> str:
    read_file = pd.read_excel(input_file)
    csv_file_name = "/tmp/temp.csv"
    read_file.to_csv(csv_file_name, index=None, header=True)
    csv_file_name = remove_first_line(csv_file_name)
    return csv_file_name


def remove_first_line(csv_file_name):
    new_file_name = "/tmp/new_csv.csv"
    with open(csv_file_name) as handle:
        lines = handle.readlines()

        print(len(lines))
        count = 0
        with open(new_file_name, "w") as handle_write:
            for line in lines:
                if count:
                    handle_write.write(line)
                count += 1
    return new_file_name


def save_items(csv_file_name, institution):
    print(f"processing {csv_file_name} {institution}")

    with open(csv_file_name) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            fecha = row['Fecha']
            fecha = datetime.strptime(fecha, '%d/%m/%Y')
            id_document, id_number = get_dni(row['Documento del visitante'])

            triad = [
                i.strip() for i in row['Funcionario visitado'].split('-')
            ]
            host_name = triad[0]
            office = " - ".join(triad[1:-1])
            host_title = triad[-1]

            lugar = row['Lugar específico']

            item = {
                'institution': institution,
                'date': fecha,
                'full_name': row['Visitante'],
                'entity': row['Entidad del visitante'],
                'reason': row['Motivo'],
                'host_name': host_name,
                "time_start": row['Hora Ingreso'],
                "time_end": row['Hora Salida'],
                "id_number": id_number,
                "id_document": id_document,
                "office": office,
                "host_title": host_title,
                "meeting_place": lugar,
            }
            item = make_hash(item)

            # get a dummy object to make hash and find in database
            dummy_item_for_hash = copy(item)
            dummy_item_for_hash['date'] = fecha.strftime('%d/%m/%Y')
            del dummy_item_for_hash['id_number']
            del dummy_item_for_hash['id_document']
            dummy_item_for_hash = make_hash(dummy_item_for_hash)
            dummy_hash = dummy_item_for_hash['sha1']

            try:
                incomplete_item = Visitor.objects.get(sha1=dummy_hash)
                incomplete_item.delete()
            except Visitor.DoesNotExist:
                pass

            save_item(item)
