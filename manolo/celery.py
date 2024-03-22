import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manolo.settings.production')

from django.conf import settings  # noqa

app = Celery('manolo_tasks', broker=settings.BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.config_from_object('django.conf:settings')
