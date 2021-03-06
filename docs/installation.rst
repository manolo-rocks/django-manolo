===========
Instalación
===========

Lo más fácil es copiar el folder django-manolo/manolo dentro de tu proyecto
Django, como si fuera una *app* adicional::

    - django_project
       - manage.py
       - django_project
       - manolo
       - otra_app

También puedes usar un ambiente virtual::

    $ mkvirtualenv django-manolo
    $ pip install django-manolo


=============
Configuración
=============

Agregar django-manolo a ``INSTALLED_APPS``
------------------------------------------

Al igual que la mayoría de apps para Django, es necesario que agregues a
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
sección de ``DATABASES`` del archivo ``settings.py``:

Ejemplo::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'manolo',
            'USER': 'INGRESAR EL NOMBRE DE USUARIO PARA POSTGRESQL',
            'PASSWORD': u'PONER LA CONTRASEÑA PARA POSTGRESQL',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

Configurar los *views*
----------------------
En tu URLconf debes agregar la siguiente línea::

    (r'^manolo/', include('manolo.urls', namespace='manolo')),

Esta configuración hará que "Manolo" funcione en el URL
``http://TUDOMINIO.com/manolo`` y funcione el buscador en la dirección
``http://TUDOMINIO.com/manolo/search``.


