FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y curl
RUN curl -L https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y gcc postgresql-client-13 libpq-dev musl-dev bash postgresql-13 postgresql-contrib && rm -rf /var/lib/apt/lists/*

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
