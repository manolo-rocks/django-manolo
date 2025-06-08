FROM docker.io/python:3.12.3-slim-bullseye as python
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y curl
RUN curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y gcc postgresql-client-14 libpq-dev musl-dev bash postgresql-14 postgresql-contrib && rm -rf /var/lib/apt/lists/*
RUN aptget install -y postgresql-common

# Google Chrome repository
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c "echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' >>   /etc/apt/sources.list"

RUN apt-get update

RUN apt-get autoremove -y
RUN mkdir /pip_requirements
ADD requirements/base.txt /base.txt
ADD requirements/production.txt /pip_requirements.txt
RUN pip install pip --upgrade
RUN pip install -r /pip_requirements.txt
COPY .env /code/.env

RUN mkdir -p /code
WORKDIR /code

ADD docker/wait_for_it.sh /wait_for_it.sh
RUN chmod +x /wait_for_it.sh

ADD . /code/
RUN ls /code

EXPOSE 8000
