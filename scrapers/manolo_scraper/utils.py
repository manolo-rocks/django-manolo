# -*- coding: utf-8 -*-
import hashlib
import re
import pkgutil
from unicodedata import normalize


def make_hash(item):
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
        # only use time and am or pm, do not include date as this is how whe
        # have done it in the past to compute the hash
        time_start_items = item['time_start'].split(' ')
        time_start = f"{time_start_items[1]} {time_start_items[2]}"
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
