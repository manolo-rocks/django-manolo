import json
import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest

from manolo.celery import app
from api.utils import process_row
from visitors.models import Visitor

log = logging.getLogger(__name__)


@app.task
def process_json_request(data) -> None:
    censored_ids = list(
        Visitor.objects.filter(censored=True)
        .distinct("id_number")
        .values_list("id_number", flat=True)
    )

    for line in data:
        item = json.loads(line)
        process_row(item, censored_ids)


@app.task
def log_task_error(
    request: HttpRequest, exc: Exception, traceback: str, institution_name: str
) -> None:
    try:
        subject = f"Manolo: Uploading {institution_name} failed"
        message = f"{request}. {exc}. {traceback}"
        from_email = settings.EMAIL_HOST_USER
        to_emails = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_emails)
    except SMTPException:
        log.exception(f"Manolo: Failed to notify log_task_error for {institution_name}.")
