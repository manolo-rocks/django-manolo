from datetime import datetime, timedelta

from testfixtures import LogCapture
from django.test import TestCase
from django.contrib.auth.models import User

from visitors.models import Subscriber, Alert, AlertDelivery, Visitor
from visitors.management.commands.send_alerts import send


class TestSendAlerts(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Yoni",
            last_name="Pacheco",
            username="yoni",
            email="noreply@example.com",
            is_active=True,
        )
        self.subscriber = Subscriber.objects.create(
            user=self.user,
            expiration=datetime.today() + timedelta(days=1)
        )
        self.alert = Alert.objects.create(
            full_name="FULANO SUTANO",
            created=datetime.now() - timedelta(days=5)
        )
        self.subscriber.alerts.add(self.alert)
        self.old_record = Visitor.objects.create(
            full_name="FULANO SUTANO",
            created=datetime.today() - timedelta(days=11)
        )
        self.new_record = Visitor.objects.create(
            full_name="FULANO SUTANO",
            created=datetime.today(),
        )
        self.alert_delivery = AlertDelivery.objects.create(
            subscriber=self.subscriber,
            alert=self.alert,
            record=self.old_record,
        )

    def test_send_alerts(self):
        with LogCapture() as log_capture:
            send()
            log_capture.check(
                ('visitors.management.commands.send_alerts', 'DEBUG', 'Sent email'),
            )
