FROM postgres:14

ENV PGDATA /srv/postgresql/data/
ADD docker/postgres/init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh
