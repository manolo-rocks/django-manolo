# -*- coding: utf8 -*-
import dataset
import codecs
import hashlib
import lib


lib.create_database()

db = dataset.connect("sqlite:///visitas.db")
table = db['visitas']

f = codecs.open("output.csv", "r", "utf8")
data = f.readlines()
f.close()


for line in data:
    line = line.strip()
    lib.insert_to_db(line)
