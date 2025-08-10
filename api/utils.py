import hashlib
import logging
from datetime import datetime
from unicodedata import normalize

from pytz import timezone

from visitors.models import Institution, Visitor

log = logging.getLogger(__name__)


def process_row(row, censored_ids=None):
    fecha = row['date']
    fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    id_document = row['id_document']
    id_number = row['id_number']

    if str(id_number) in censored_ids:
        log.info(f"Skipping censored id_number {id_number}")
        return

    # if row.get('institution') == 'municipalidad de lima':
    #     host_name = row['host_name']
    #     host_title = row['host_title']
    #     office = row['office']
    # else:
    try:
        host_name, office, host_title = row['host_name'].split(' - ')
    except ValueError:
        try:
            host_name, office = row['host_name'].split(' - ')
            host_title = ''
        except ValueError:
            host_name = row['host_name']
            office = ''
            host_title = ''

    try:
        institution = Institution.objects.get(ruc=row['institution_ruc'])
    except Institution.DoesNotExist:
        log.exception(f"Could not find institution with ruc {row['institution_ruc']} {fecha}")
        return

    item = {
        'date': fecha,
        "id_document": id_document,
        "id_number": id_number,
        'host_name': host_name,
        'full_name': row['full_name'],
        "time_start": row['time_start'],
        "time_end": row['time_end'],
        'reason': row.get('reason') or "",
        'entity': row['entity'],
        "location": row.get("location") or "",
        "office": office,
        "host_title": host_title,
        "meeting_place": row['meeting_place'],
        'institution': institution.slug,
    }
    item = make_hash(item)
    save_item(item)


def make_hash(item):
    """Create a sha1 hash and add it to item

    It requires the following keys:

    institution
    full_name
    id_document
    id_number
    time_start
    date: %Y-%m-%d  it should be a string
    """
    hash_input = ''
    hash_input += str(item['institution'])

    if 'full_name' in item:
        hash_input += str(normalize('NFKD', item['full_name']))

    if 'id_document' in item:
        hash_input += str(normalize('NFKD', item['id_document']))

    if 'id_number' in item:
        hash_input += str(normalize('NFKD', item['id_number']))

    if isinstance(item['date'], str):
        hash_input += str(item['date'])
    else:
        hash_input += str(item['date'].strftime("%Y-%m-%d"))

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


def save_item(item):
    """
    returns error if occurred otherwise returns None
    """

    lima = timezone('America/Lima')

    try:
        visitor_queryset = Visitor.objects.filter(sha1=item['sha1'])
    except Exception as e:
        raise Exception(f"Could not search in the database: {e}")

    if not visitor_queryset.exists():
        item['created'] = datetime.now(lima)
        item['modified'] = datetime.now(lima)
        institution2 = Institution.objects.get(slug=item['institution'])
        item['institution2'] = institution2

        try:
            Visitor.objects.create(**item)
            print('saving to db item')
        except Exception as e:
            print(f'Error when saving item to database {e}')

    elif visitor_queryset.exists() and not visitor_queryset.first().time_end:
        if item['time_end']:
            visitor = visitor_queryset.first()
            visitor.time_end = item['time_end']
            visitor.save()
            print(f"Updating date: {item['date']} is found in db")

    else:
        print("{0}, date: {1} is found in db, not saving".format(item['sha1'], item['date']))
