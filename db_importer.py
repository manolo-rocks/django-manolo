"""
Import data from django-manolo database into Manolo-v2
"""
import codecs
import dataset
import datetime
import json
import hashlib
import re
import sys
import os.path
import argparse
from unidecode import unidecode

import pyprind


def get_db_credentials(settings):
    if settings == 'local':
        from manolo.settings.local import DATABASES
        return DATABASES['default']
    if settings == 'production':
        from manolo.settings.production import DATABASES
        return DATABASES['default']


def get_tables_from_source_db(input_db):
    db = dataset.connect("sqlite:///" + input_db)
    return db.tables


class Importer(object):
    def __init__(self, input_json, settings, limit, verbosity):
        self.items = []
        self.mytable = ''
        self.verbosity = verbosity
        self.limit = limit
        self.input_json = input_json
        self.settings = settings
        self.ids_seen = self.get_ids_from_db()

    def get_ids_from_db(self):
        ids_seen = set()

        credentials = get_db_credentials(self.settings)
        if 'sqlite3' in credentials['ENGINE']:
            db = dataset.connect("sqlite:///" + os.path.basename(credentials['NAME']))
        if 'postgresql' in credentials['ENGINE']:
            db = dataset.connect('postgresql://' +
                                 credentials['USER'] + ':' +
                                 credentials['PASSWORD'] + '@' +
                                 credentials['HOST'] + ':' +
                                 credentials['PORT'] + '/' +
                                 credentials['NAME'])
        res = db.query("select sha1 from visitors_visitor")
        if res:
            for i in res:
                ids_seen.add(i['sha1'])
        return ids_seen

    def import_json(self):
        with open(self.input_json) as handle:
            for line in handle:
                item = line.strip()
                item = self.parse_item(json.loads(item))
                if item['sha1'] in self.ids_seen:
                    if self.verbosity:
                        print("Duplicate item found: %s" % item['sha1'])
                else:
                    self.ids_seen.add(item['sha1'])
                    self.items.append(item)

    def parse_item(self, item):
        if 'id' in item:
            del item['id']

        if 'num_visit' in item:
            del item['num_visit']

        if 'visitor' in item:
            item['full_name'] = re.sub("\s+", " ", item['visitor']).strip()
            del item['visitor']

        if 'procedence' in item:
            if item['procedence'] != '':
                item['entity'] = item['procedence']
            del item['procedence']

        if 'entity' not in item:
            item['entity'] = ''

        if 'office' not in item:
            item['office'] = ''

        if 'host' in item:
            item['host_name'] = re.sub("\s+", " ", item['host']).strip()
            del item['host']

        item['location'] = ''
        if 'sede' in item:
            if item['sede'] != '':
                item['location'] = item['sede']
            del item['sede']

        if 'objective' in item:
            item['reason'] = item['objective']
            del item['objective']

        if 'observation' in item:
            del item['observation']

        if 'meeting_place' not in item:
            item['meeting_place'] = ''

        if 'sha512' in item:
            del item['sha512']

        item['sha1'] = make_hash(
            item['institution'],
            item['full_name'],
            item['id_document'],
            item['id_number'],
            item['date'],
            item['time_start']
        )
        return item

    def bulk_upload(self):
        items_to_upload = []
        append = items_to_upload.append

        credentials = get_db_credentials(self.settings)
        if 'sqlite3' in credentials['ENGINE']:
            db = dataset.connect("sqlite:///" + os.path.basename(credentials['NAME']))
        if 'postgresql' in credentials['ENGINE']:
            db = dataset.connect('postgresql://' +
                                 credentials['USER'] + ':' +
                                 credentials['PASSWORD'] + '@' +
                                 credentials['HOST'] + ':' +
                                 credentials['PORT'] + '/' +
                                 credentials['NAME'])
        table = db['visitors_visitor']

        print("Starting checks to see if we have this item in our database.")
        if len(self.items) == 0:
            print("Nothing to upload")
        else:
            for i in pyprind.prog_bar(range(len(self.items))):
                item = self.items[i]
                try:
                    item['date'] = datetime.datetime.strptime(
                        item['date'],
                        '%Y-%m-%d',
                        )
                except ValueError:
                    item['date'] = None

                append(item)

            print("uploading %i records for table %s" % (len(items_to_upload), self.mytable))

            table.insert_many(items_to_upload)


def make_hash(institution, full_name, id_document, id_number, date, time_start):
    hash_input = str(
        str(institution) +
        str(unidecode(full_name)) +
        str(unidecode(id_document)) +
        str(unidecode(id_number)) +
        str(date) +
        str(time_start)
    )
    hash_output = hashlib.sha1()
    hash_output.update(hash_input.encode('utf-8'))
    return hash_output.hexdigest()


def import_from_json(input_json, settings, limit, verbosity):
    importer = Importer(input_json, settings, limit, verbosity)
    importer.import_json()
    importer.bulk_upload()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Imports manolo_v1 database into v2')
    parser.add_argument('-j', '--json', metavar='json',
                        required=False,
                        help='Import from JSONlines file')
    parser.add_argument('-s', '--settings', metavar='settings',
                        required=True,
                        choices=['local', 'production'],
                        help='Data should be imported to local or production database?')
    parser.add_argument('-l', '--limit', metavar='limit',
                        required=False,
                        help='Limits the number of items to import. Needs integer.')
    parser.add_argument('-v', '--verbosity', metavar='verbosity',
                        required=False,
                        help='Prints to screen: 0 or 1')
    args = parser.parse_args()

    if args.verbosity is None:
        verbosity = False
    elif args.verbosity == '0':
        verbosity = False
    else:
        verbosity = True

    if args.limit is None:
        limit = False
    else:
        limit = int(args.limit)

    if args.json is None:
        print("You need to enter either a Jsonlines file.")
        sys.exit(1)

    import_from_json(args.json, args.settings, limit, verbosity)
