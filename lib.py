# -*- coding: utf8 -*-

import dataset
import os
import config
import hashlib

def insert_to_db(line):
    db = dataset.connect("sqlite:///visitas.db")
    table = db['visitas']
    
    # line is a line of downloaded data
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

    my_string = str(item['date']) + str(item['id_document']) + str(item['time_start'])
    m = hashlib.md5()
    m.update(my_string)
    
    item['md5_hash'] = str(m.hexdigest())

    if not table.find_one(md5_hash=item['md5_hash']):
        print "uploading %s" % str(item['md5_hash'])
        table.insert(item)

def create_database():
    print "Creating database"
    database_file = os.path.join(config.base_folder, "visitas.db")
    if not os.path.isfile(database_file):
        try:
            db = dataset.connect('sqlite:///visitas.db')
            table = db.create_table("visitas")
            table.create_column('md5_hash', sqlalchemy.Text)
            table.create_column('date', sqlalchemy.String)
            table.create_column('visitor', sqlalchemy.Text)
            table.create_column('id_document', sqlalchemy.String)
            table.create_column('entity', sqlalchemy.Text)
            table.create_column('objective', sqlalchemy.Text)
            table.create_column('host', sqlalchemy.Text)
            table.create_column('office', sqlalchemy.Text)
            table.create_column('meeting_place', sqlalchemy.Text)
            table.create_column('time_start', sqlalchemy.Time)
            table.create_column('time_end', sqlalchemy.Time)
        except:
            pass

def main():
    print ""

if __name__ == "__main__":
    main()
