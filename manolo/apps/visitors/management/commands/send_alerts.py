import logging
from smtplib import SMTPException

from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from visitors.models import Alert, Visitor, AlertDelivery


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Command(BaseCommand):
    def handle(self, *args, **options):
        send()


def send():
    alerts = Alert.objects.all()
    delivered_alerts = AlertDelivery.objects.all().values_list("record", flat=True)
    for alert in alerts:
        # visitors created later than alert and not in AlertDelivery
        visitors = Visitor.objects.filter(
            full_name=alert.full_name,
            created__gte=alert.created,
        ).exclude(id__in=delivered_alerts)
        subscribers = alert.subscriber_set.all()
        if visitors:
            for visitor in visitors:
                for subscriber in subscribers:
                    # send mail
                    logger.debug("Sent email")
                    AlertDelivery.objects.create(
                        subscriber=subscriber,
                        alert=alert,
                        record=visitor,
                    )
                    notify(visitor, subscriber)


def notify(visitor, subscriber):
    logger.debug("notify_subscriber {}".format(subscriber))

    subject = "Manolo Alerta: {}".format(visitor.full_name)
    content = "Manolo Alerta: Nuevos registros para visitante {}\n\n".format(visitor.full_name)
    content += "<a href='https://manolo.rocks/search/?q={0}'>{0}</a>".format(
        visitor.full_name)
    from_email = 'noreply@manolo.rocks'

    to_emails = [subscriber.user.email]
    try:
        send_mail(subject, content, from_email, to_emails)
    except SMTPException:
        logger.exception("Failed to notify_list_users for subscriber " + str(subscriber))
    else:
        logger.debug("sent alert to " + str(to_emails))
