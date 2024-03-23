from celery import Celery
from django.conf import settings  # noqa
from kombu import Exchange, Queue

default_exchange = Exchange('default', type='direct')

app = Celery('manolo_tasks', broker=settings.BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.task_track_started = True
app.conf.task_ignore_result = False
app.conf.task_queues = (
    Queue('default', default_exchange, routing_key='default'),
)
app.config_from_object('django.conf:settings')
