import datetime

from w3lib.html import remove_tags
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def filter_date(value):
    if isinstance(value, datetime.datetime):
        return datetime.date.strftime(value, '%Y-%m-%d')

    return value


class ManoloItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags)
    default_output_processor = TakeFirst()
