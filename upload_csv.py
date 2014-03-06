# -*- coding: utf8 -*-
import dataset
import codecs
import lib


lib.create_database()

db = dataset.connect("sqlite:///visitas.db")
table = db['visitas']

f = codecs.open("output.csv", "r", "utf8")
data = f.readlines()
f.close()

items = []
for line in data:
    line = line.strip()
    i = line.split(",")
    item = dict()
    item['date'] = i[0]
    item['visitor'] = i[1]
    item['id_document'] = i[2]
    item['entity'] = i[3]
    item['objective'] = i[4]
    item['host'] = i[5]
    item['office'] = i[6]
    item['meeting_place'] = i[7]
    item['time_start'] = i[8]
    item['time_end'] = i[9]

    items.append(item)

print len(items)
table.insert_many(items)
