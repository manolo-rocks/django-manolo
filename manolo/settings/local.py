from .base import *


ADMINS = (
    ('AniversarioPeru', 'aniversarioperu1@gmail.com'),
)

LOCAL_APPS = (
    'debug_toolbar',
)

INSTALLED_APPS += LOCAL_APPS

MANAGERS = ADMINS
