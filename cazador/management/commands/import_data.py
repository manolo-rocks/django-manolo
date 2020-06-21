"""Add deudores al Estado to index"""
from tqdm import tqdm

from django.core.management.base import BaseCommand, CommandError

from cazador.models import Cazador
from cazador import shrink_url_in_string



DBS = ['deudores', 'candidato_2014', 'narcoindultos', 'redam']


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-i',
                            action='store',
                            dest='input_file',
                            help='Enter filename with data to import.',
                            )
        parser.add_argument('-db',
                            action='store',
                            dest='database',
                            help='Enter database, options: {}'.format(
                            ', '.join(DBS)))

    def handle(self, *args, **options):
        if not options['input_file']:
            raise CommandError("Input Filename does not exist.")
        if options['database'] not in DBS:
            raise CommandError("Name of database is incorrect. Use one of the "
                               "following options: {}".format(
                               ', '.join(DBS)))

        input_file = options['input_file']
        database = options['database']
        self.process_file(input_file, database)

    def process_file(self, input_file, database):
        print(input_file, database)
        with open(input_file, "r") as handle:
            data = handle.readlines()

        entries = []
        for raw_line in tqdm(data):
            line = raw_line.strip()
            fields = line.split("\t")
            if database == 'candidato_2014':
                raw_data = " ".join([fields[2], fields[3], fields[4], fields[1], fields[7]])
                c = Cazador(
                        raw_data=raw_data,
                        raw_data_with_short_links=shrink_url_in_string(raw_data),
                        source=database,
                )
            elif database == 'redam':
                c = Cazador(
                        raw_data=", ".join(fields),
                        source=database,
                )
            elif database == 'narcoindultos':
                c = Cazador(
                        raw_data=" ".join(fields),
                        source=database,
                )
            else:
                raw_data = " ".join([fields[2], fields[10], fields[1]])
                c = Cazador(
                        raw_data=raw_data,
                        raw_data_with_short_links=shrink_url_in_string(raw_data),
                        source=database,
                )
            entries.append(c)
        Cazador.objects.bulk_create(entries)
