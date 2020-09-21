import datetime

from django import forms
from django.conf import settings

from manolo.settings.production import PREMIUM_INSTITUTIONS
from visitors.models import Visitor
from visitors.utils import is_dni


class ManoloForm(forms.Form):
    def search(self, premium):
        if settings.ELASTICSEARCH_ENABLED:
            if not self.is_valid() or not self.cleaned_data.get('q'):
                return self.no_query_found()

            sqs = super(ManoloForm, self).search()
            sqs = self.searchqueryset.using('default').auto_query(self.cleaned_data['q']).order_by('-date')
            if not premium:
                today = datetime.datetime.today()
                six_months_ago = today - datetime.timedelta(days=180)
                sqs = sqs.filter(date__lte=six_months_ago)
                for institution in PREMIUM_INSTITUTIONS:
                    sqs = sqs.exclude(institution=institution)

            if self.load_all:
                sqs = sqs.load_all()
        else:
            # use querysets
            keywords = self.data['q']
            if is_dni(keywords):
                sqs = Visitor.objects.filter(
                    id_number__contains=keywords
                ).order_by('-date')
            else:
                sqs = Visitor.objects.filter(
                    full_name__icontains=keywords
                ).order_by('-date')
        return sqs

