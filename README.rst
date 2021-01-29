Django-manolo
=============

|Pypi index| |Build Status| |Dependencies status| |Cover alls|

Manolo, buscador de lobistas
============================

Presento un buscador de personas que ingresan las oficinas de
entidades del Estado peruano.
http://manolo.rocks

Motivación
==========

Todo aquel que visita el Organismo de Contrataciones debe registrarse
dejando su **nombre, documento de identidad, motivo de visita, empleado
público que lo recibe, hora de ingreso, salida y fecha**. Toda esta
información está disponible en la Internet en esta dirección:
http://visitas.osce.gob.pe/controlVisitas/index.php?r=consultas/visitaConsulta/index

El problema es que la interfaz no es muy amigable y sólo se pueden
buscar visitantes a la institución por día. Seleccionas cualquier día
del menú y veras todos los visitantes que de esa fecha. Si quieres saber
cuántas veces ha visitado el lugar una determinada persona, debes buscar
día por día, página por página, revisar línea por línea en búsqueda de
la persona de interés.

Obviamente este tipo de búsqueda es muy tedioso, aburrido, inexacto (se
presta a errores de conteo) además que toma demasiado tiempo hacer una
simple búsqueda.

Por eso decidí construir un simple buscador de personas que visitan
dicha institución estatal. La función de este buscador simple: **Tipeas
un nombre y aparecerán en pantalla todas las veces que la persona tenga
ingresos registrados al Organismo de Contrataciones.**

A partir de Manolo versión 2.0.0, la versión online (en http://manolo.rocks)
contiene una base de datos unificada conteniendo registro de visitas de 7
entidades del Estado peruano.

Crea tu propio buscador de lobistas
===================================
Ahora "Manolo" es un plugin para Django. Puedes crear rápidamente un
buscador de lobistas para tu institución estatal favorita. Para eso
necesitas conseguir el link donde esté alojado el registro de visitas de la
institución. Se lo das a Manolo y él hará lo suyo.

Más información en un post en el blog Útero de Marita:

http://aniversarioperu.utero.pe/2014/03/08/manolo-buscador-de-lobistas/

Esta es la dirección web de **Manolo, buscador de personas**:
http://manolo.rocks

Documentación
=============

"Manolo" es un paquete o *app* para Django y puede ser agregado
fácilmente a algún proyecto de Django a manera de plugin.

La documentación completa está en este enlace:
https://django-manolo.readthedocs.org.

Fork from Gihub
==================
Aquí puedes seguir el desarrollo de Manolo
https://github.com/aniversarioperu/django-manolo


Install
=======

1. `pip install -r requirements.txt`.
2. Create a config file called `config.json`. See Configure section.
3. `python manage.py syncdb --settings=manolo.settings.local`
4. `python manage.py migrate --settings=manolo.settings.local`
5. `python manage.py runserver --settings=manolo.settings.local`.

Note: This project uses python 3.4

Install (using Docker)
======================

Setup local environment using docker

System Requirements
-------------------

- `Docker Desktop <https://www.docker.com/products/docker-desktop>`_ (docker-engine >= 17.12.0)

Setup
-----
::

    # STEP 1: Create .env file from template
    $ cp env.dist .env

    # STEP 2: Open & enter values.
    $ vi .env

    # STEP 3: Build and spin up local container
    $ bash docker/docker_compose -f docker-compose.local.yml up

    # NOTE: Open another terminal starting here
    # STEP 4: Apply migrations
    $ bash docker/docker_compose -f docker-compose.local.yml exec app python manage.py migrate

    # STEP 5. Create superuser account
    $ bash docker/docker_compose -f docker-compose.local.yml exec app python manage.py createsuperuser

    # STEP 5. Load fixtures
    $ bash docker/docker_compose -f docker-compose.local.yml exec app python manage.py loaddata institutions

    # STEP 5. Collect static resources
    $ bash docker/docker_compose -f docker-compose.local.yml exec app python manage.py collectstatic

    # NOTE: The following two steps (6 & 7) pretend to fill DB with some
    # data so the site has something to visualize, however these commands are
    # executed periodically via scheduled tasks.

    # STEP 6. Pull visitors from institutions into DB. This may take several mins (> 30)
    $ bash docker/docker_compose -f docker-compose.local.yml exec cron /etc/cron.daily/run_all_scrapers.sh

    # STEP 7. Recompute statistics
    $ bash docker/docker_compose -f docker-compose.local.yml exec app python manage.py run_statistics


Site is available at http://localhost:4082

Troubleshooting
===============
TBD

Configure
=========
Create a `.env` file locally to keep all private credentials protected: 

::

    DEBUG=on
    SECRET_KEY=your-secret-key
    DATABASE_URL=psql://user:un-githubbedpassword@127.0.0.1:8458/database


Releases
========

* 2018-07-22. Changed suscription to credit based

.. |Pypi index| image:: https://badge.fury.io/py/django-manolo.svg
   :target: https://badge.fury.io/py/django-manolo
.. |Build Status| image:: https://travis-ci.org/manolo-rocks/django-manolo.png?branch=master
   :target: https://travis-ci.org/manolo-rocks/django-manolo
.. |Cover alls| image:: https://coveralls.io/repos/manolo-rocks/django-manolo/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/manolo-rocks/django-manolo?branch=master
.. |Dependencies status| image:: https://gemnasium.com/badges/github.com/manolo-rocks/django-manolo.svg
   :target: https://gemnasium.com/github.com/manolo-rocks/django-manolo
