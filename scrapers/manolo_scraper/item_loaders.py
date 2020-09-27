import datetime

from scrapy.utils.markup import remove_tags
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose


def filter_date(date):
    if isinstance(date, datetime.datetime):
        return datetime.date.strftime(date, '%Y-%m-%d')

    return date


class ManoloItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, filter_date)