# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import logging
import re

from scrapy.exceptions import DropItem

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
    def process_item(self, item, spider):
        for k, v in item.items():
            if isinstance(v, str) is True:
                value = re.sub(r'\s+', ' ', v)
                item[k] = value.strip()
            else:
                item[k] = v
        try:
            item['date'] = datetime.date.strftime(item['date'], '%Y-%m-%d')
        except TypeError as e:
            print("Our date is good, continue: {}".format(e))

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

        if not 'full_name' in item:
            raise DropItem("Missing visitor in item: {}".format(item))

        if item['full_name'] == '':
            raise DropItem("Missing visitor in item: {}".format(item))

        if 'HORA DE' in item['time_start']:
            raise DropItem("This is a header, drop it: {}".format(item))

        return item

    def save_item(self, item):
        if not Visitor.objects.filter(sha1=item['sha1']).exists():
            item['created'] = datetime.datetime.now()
            item['modified'] = datetime.datetime.now()
            record = Visitor(item)
            record.save()
            logging.info("Saving: {0}, date: {1}".format(item['sha1'], item['date']))
        else:
            logging.info("{0}, date: {1} is found in db, not saving".format(item['sha1'], item['date']))
