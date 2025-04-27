# -*- coding: utf-8 -*-
import logging
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import re

from scrapy.exceptions import DropItem

from api.utils import process_row, save_item

log = logging.getLogger(__name__)


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
