# -*- coding: utf-8 -*-

"""
test_django-manolo
------------

Tests for `django-manolo` models module.
"""
import datetime
from datetime import timedelta as td
import unittest

import dataset
import sqlalchemy

from django.conf import settings

from manolo.models import Manolo
from manolo.management.commands.scraper import Command


class TestManolo(unittest.TestCase):

    def setUp(self):
        db = dataset.connect('sqlite:///' + settings.DATABASES['default']['NAME'])
        table = db['manolo_manolo']
        table.create_column('office', sqlalchemy.String(length=250))
        table.create_column('sha512', sqlalchemy.String(length=200))
        table.create_column('visitor', sqlalchemy.String(length=250))
        table.create_column('meeting_place', sqlalchemy.String(length=250))
        table.create_column('host', sqlalchemy.String(length=250))
        table.create_column('entity', sqlalchemy.String(length=250))
        table.create_column('objective', sqlalchemy.String(length=250))
        table.create_column('id_document', sqlalchemy.String(length=250))
        table.create_column('date', sqlalchemy.Date())
        table.create_column('time_start', sqlalchemy.String(length=100))
        table.create_column('time_end', sqlalchemy.String(length=100))

        Manolo.objects.get_or_create(date=None)
        Manolo.objects.get_or_create(date=datetime.date(2011, 7, 28))
        Manolo.objects.get_or_create(date=datetime.date.today())

    def test_get_last_date_in_db(self):
        d1 = Command()
        d1.__init__()
        result = d1.get_last_date_in_db() + td(3)
        self.assertEqual(result, datetime.date.today())
