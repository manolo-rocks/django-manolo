# -*- coding: utf8 -*-
import dataset
import codecs
import lib
import hashlib

db = dataset.connect("sqlite:///visitas.db")
table = db['visitas']

    
lib.create_database()
items = lib.get_data()
table.insert_many(items)
