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
    def __init__(self, input_db, settings, limit, verbosity):
        self.ids_seen = set()
        self.items = []
        self.mytable = ''
        self.verbosity = verbosity
        self.limit = limit
        self.input_db = input_db
        self.settings = settings

    def get_table(self, mytable):
        self.mytable = mytable

        db = dataset.connect("sqlite:///" + self.input_db)

        if self.limit:
            res = db.query("select * from " + mytable + " limit %i" % limit)
        else:
            res = db.query("select * from " + mytable)

        for item in res:
            item = self.parse_item(item)

        if item['sha1'] in self.ids_seen:
            if self.verbosity:
                print("Duplicate item found: %s" % item['sha1'])
                print(item)
        else:
            self.ids_seen.add(item['sha1'])
            self.items.append(item)

    def import_json(self):
        with open(self.input_db) as handle:
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

        item['full_name'] = re.sub("\s+", " ", item['visitor']).strip()
        del item['visitor']

        if 'procedence' in item:
            if item['procedence'] != '':
                item['entity'] = item['procedence']
            del item['procedence']

        item['host_name'] = re.sub("\s+", " ", item['host']).strip()
        del item['host']

        item['location'] = ''
        if 'sede' in item:
            if item['sede'] != '':
                item['location'] = item['sede']
            del item['sede']

        item['reason'] = item['objective']
        if 'observation' in item:
            del item['observation']

        if 'id_number' in item:
            item['id_document'], item['id_number'] = self.get_dni(item['id_number'])
        else:
            item['id_document'], item['id_number'] = self.get_dni(item['id_document'])

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

    def get_dni(self, document_identity):
        id_document = ''
        id_number = ''

        document_identity = document_identity.replace(':', ' ')
        document_identity = re.sub('\s+', ' ', document_identity)
        document_identity = document_identity.strip()
        document_identity = re.sub('^', ' ', document_identity)

        res = re.search("(.*)\s(([A-Za-z0-9]+\W*)+)$", document_identity)
        if res:
            id_document = res.groups()[0].strip()
            id_number = res.groups()[1].strip()

        if id_document == '':
            id_document = 'DNI'

        return id_document, id_number

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
        for i in pyprind.prog_bar(range(len(self.items))):
            item = self.items[i]
            res = table.find_one(sha1=item['sha1'])
            if res is None:
                try:
                    item['date'] = datetime.datetime.strptime(
                                                              item['date'],
                                                              '%Y-%m-%d',
                                                              )
                except ValueError:
                    item['date'] = None

                append(item)
            else:
                if self.verbosity:
                    print("already in db %s" % item['sha1'])

        print("uploading %i records for table %s" % (len(items_to_upload), self.mytable))

        table.insert_many(items_to_upload)


def make_hash(institution, full_name, id_document, id_number, date, time_start):
    hash_input = str(
        str(institution) +
        str(unidecode(full_name)) +
        str(id_document) +
        str(id_number) +
        str(date) +
        str(time_start)
    )
    hash_output = hashlib.sha1()
    hash_output.update(hash_input.encode('utf-8'))
    return hash_output.hexdigest()


def import_data(input_db, settings, limit, verbosity):
    for mytable in get_tables_from_source_db(input_db):
        if mytable.startswith("manolo"):
            importer = Importer(input_db, settings, limit, verbosity)
            importer.get_table(mytable)

            print("%i items will be imported for table %s" % (len(importer.items), mytable))
            importer.import_table()


def import_from_json(input_db, settings, limit, verbosity):
    importer = Importer(input_db, settings, limit, verbosity)
    importer.import_json()
    importer.bulk_upload()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Imports manolo_v1 database into v2')
    parser.add_argument('-i', '--input_db', metavar='input_db',
                        required=False,
                        help='SQlite3 database from Manolo_v1 to import')
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

    if args.json is None and args.input_db is None:
        print("You need to enter either a Sqlite3 database file or Jsonlines file.")
        sys.exit(1)

    import_from_json(args.input_db, args.settings, limit, verbosity)
