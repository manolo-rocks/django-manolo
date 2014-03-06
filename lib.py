def create_database():
    print "Creating database"
    database_file = os.path.join(config.base_folder, "visita.db")
    if not os.path.isfile(database_file):
        try:
            db = dataset.connect('sqlite:///visita.db')
            table = db.create_table("visita")
            table.create_column('date', sqlalchemy.String)
            table.create_column('visitor', sqlalchemy.String)
            table.create_column('id_document', sqlalchemy.String)
            table.create_column('entity', sqlalchemy.Text)
            table.create_column('objective', sqlalchemy.String)
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
