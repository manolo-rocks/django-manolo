import re
import pkgutil

from api.utils import make_hash


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


def get_dni(document_identity):
    id_document = ''
    id_number = ''

    document_identity = document_identity.replace(':', ' ')
    document_identity = re.sub(r'\s+', ' ', document_identity)
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
