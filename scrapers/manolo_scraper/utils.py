# -*- coding: utf-8 -*-
import hashlib
import re
import pkgutil
from unicodedata import normalize


def update_hash_from_visitor(visitor):
    sha1_hash = make_hash_from_visitor(visitor)
    visitor.sha1 = sha1_hash
    visitor.save()


def make_hash_from_visitor(visitor):
    item = {
        "institution": visitor.institution,
        "full_name": visitor.full_name,
        "id_document": visitor.id_document,
        "id_number": visitor.id_number,
        "time_start": visitor.time_start,
        "date": visitor.date.strftime("%Y-%m-%d")
    }
    item = make_hash(item)
    return item["sha1"]


def make_hash(item):
    """Create a sha1 hash and add it to item

    It requires the following keys:

    institution
    full_name
    id_document
    id_number
    time_start
    date: %d/%m/%Y
    """
    hash_input = ''
    hash_input += str(item['institution'])

    if 'full_name' in item:
        hash_input += str(normalize('NFKD', item['full_name']))

    if 'id_document' in item:
        hash_input += str(normalize('NFKD', item['id_document']))

    if 'id_number' in item:
        hash_input += str(normalize('NFKD', item['id_number']))

    hash_input += str(item['date'])

    if 'time_start' in item:
        # only use time and am or pm, do not include date as this is how we
        # have done it in the past to compute the hash
        time_start_items = item['time_start'].split(' ')
        if len(time_start_items) == 3:
            time_start = f"{time_start_items[1]} {time_start_items[2]}"
        else:
            time_start = item['time_start']

        hash_input += str(normalize('NFKD', time_start))

    hash_output = hashlib.sha1()
    hash_output.update(hash_input.encode("utf-8"))
    item['sha1'] = hash_output.hexdigest()
    return item


def get_dni(document_identity):
    id_document = ''
    id_number = ''

    document_identity = document_identity.replace(':', ' ')
    document_identity = re.sub('\s+', ' ', document_identity)
    document_identity = document_identity.strip()
    document_identity = re.sub('^', ' ', document_identity)

    res = re.search(r"(.*)\s(([A-Za-z0-9]+\W*)+)$", document_identity)
    if res:
        id_document = res.groups()[0].strip()
        id_number = res.groups()[1].strip()

    if id_document == '':
        id_document = 'DNI'

    return id_document, id_number


def get_this_month(number):
    months = {
        '01': 'enero',
        '02': 'febrero',
        '03': 'marzo',
        '04': 'abril',
        '05': 'mayo',
        '06': 'junio',
        '07': 'julio',
        '08': 'agosto',
        '09': 'setiembre',
        '10': 'octubre',
        '11': 'noviembre',
        '12': 'diciembre',
    }
    return months[number]


def get_lua_script(script_name, dependencies=None):
    dependencies_script = ''
    if dependencies:
        for file_name in dependencies:
            dependencies_script += pkgutil.get_data(
                "manolo_scraper", "splash/{}".format(file_name))

    lua_script = pkgutil.get_data(
        "manolo_scraper", "splash/{}".format(script_name))

    return dependencies_script + lua_script
