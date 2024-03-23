FROM postgres:15-bullseye

ENV PGDATA /srv/postgresql/data/
ADD docker/postgres/init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh
