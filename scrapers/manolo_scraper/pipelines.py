# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import re

from pytz import timezone
from scrapy.exceptions import DropItem

from scrapers.manolo_scraper.utils import make_hash
from visitors.models import Visitor


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['sha1'] in self.ids_seen:
            raise DropItem("Duplicate item found: {}".format(item))
        else:
            self.ids_seen.add(item['sha1'])
            return item


class CleanItemPipeline(object):
    errors = []

    def open_spider(self, spider):
        self.errors = []

    def close_spider(self, spider):
        # TODO: send an email if error where found
        print(f'Found {len(self.errors)} errors: {self.errors}')

    def process_item(self, item, spider):
        result = process_item(item)
        item = result['item']
        error = result['error']

        if error:
            self.errors.append(error)
        return item


def process_items(items):
    for item in items:
        process_row(item)


def process_item(item):
    """Process and saves a scraped item"""
    for k, v in item.items():
        if isinstance(v, str) is True:
            value = re.sub(r'\s+', ' ', v)
            item[k] = value.strip()
        else:
            item[k] = v

    item['date'] = item['date'].replace(' 00:00:00', '')
    try:
        item['date'] = datetime.strptime(item['date'], '%d/%m/%Y')
    except ValueError:
        try:
            item['date'] = datetime.strptime(item['date'], '%Y-%m-%d')
        except ValueError as e:
            print('***', e)

    if 'time_end' not in item:
        item['time_end'] = ''

    if 'meeting_place' not in item:
        item['meeting_place'] = ''

    if 'location' not in item:
        item['location'] = ''

    if 'office' not in item:
        item['office'] = ''

    if 'entity' not in item:
        item['entity'] = ''

    if 'full_name' not in item:
        raise DropItem("Missing visitor in item: {}".format(item))

    if item['full_name'] == '':
        raise DropItem("Missing visitor in item: {}".format(item))

    if 'HORA DE' in item['time_start']:
        raise DropItem("This is a header, drop it: {}".format(item))

    try:
        saving_error = save_item(item)
    except Exception as e:
        saving_error = f"Could not store in the database: {e}"
        print(saving_error)

    return {
        'error': saving_error,
        'item': item,
    }


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


def process_row(row):
    fecha = row['date']
    fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    id_document = row['id_document']
    id_number = row['id_number']
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

    item = {
        'full_name': row['full_name'],
        'entity': row['entity'],
        "id_number": id_number,
        "id_document": id_document,
        'host_name': host_name,
        "office": office,
        "host_title": host_title,
        'reason': row['reason'],
        "meeting_place": row['meeting_place'],
        'institution': row['institution'],
        "time_start": row['time_start'],
        "time_end": row['time_end'],
        "location": row.get("location"),
        'date': fecha,
    }
    item = make_hash(item)
    save_item(item)
