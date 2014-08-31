===========
Instalación
===========

En un terminal tipear lo siguiente::

    $ pip install django-manolo

También puedes usar un ambiente virtual::

    $ mkvirtualenv django-manolo
    $ pip install django-manolo


=============
Configuración
=============

Agregar django-manolo a ``INSTALLED_APPS``
------------------------------------------

Al igual que la mayoría de apps para Django, es necesario que agreges a
``manolo`` en la lista de ``INSTALLED_APPS`` dentro de tu archivo
``settings.py``.

Ejemplo::

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',

        # Agregado
        'manolo',

        # Luego tu apps usuales...
        'blog',
    ]


Modifica tu archivo ``settings.py``
-----------------------------------

En el archivo ``settings.py`` es necesario que agregues la información de la
base de datos a utilizar. ``Manolo`` ha sido desarrollado con la base de
datos relacional ``Postgresql``.

Es necesario instalar ``Postgresql`` en tu computadora y crear una base de
datos llamada ``manolo``. Luego debes agregar los datos necesarios en la
seccion de ``DATABASES`` del archivo ``settings.py``:

Ejemplo::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'manolo',
            'USER': 'ani',
            'PASSWORD': get_secret("POSTGRESQL_PASSWORD"),
            'HOST': 'localhost',
            'PORT': '',
        }
    }

En progreso
-----------

continuará...