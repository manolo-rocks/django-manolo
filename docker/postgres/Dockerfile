FROM docker.io/postgres:14-bullseye

ENV PGDATA /srv/postgresql/data/
ADD docker/postgres/init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh
RUN chmod +x /docker-entrypoint-initdb.d/init-user-db.sh
