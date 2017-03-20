import logging

from django.core.management.base import BaseCommand

from visitors.models import Alert, Visitor, AlertDelivery


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Command(BaseCommand):
    def handle(self, *args, **options):
        send()


def send():
    alerts = Alert.objects.all()
    delivered_alerts = AlertDelivery.objects.all().values_list("id", flat=True)
    for alert in alerts:
        # visitors created later than alert and not in AlertDelivery
        visitors = Visitor.objects.filter(created__gte=alert.created).exclude(id__in=delivered_alerts)
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
