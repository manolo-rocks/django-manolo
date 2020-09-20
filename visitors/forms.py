import datetime

from django import forms

from manolo.settings.production import PREMIUM_INSTITUTIONS


class ManoloForm(forms.Form):
    def search(self, premium):
        sqs = super(ManoloForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self.searchqueryset.using('default').auto_query(self.cleaned_data['q']).order_by('-date')
        if not premium:
            today = datetime.datetime.today()
            six_months_ago = today - datetime.timedelta(days=180)
            sqs = sqs.filter(date__lte=six_months_ago)
            for institution in PREMIUM_INSTITUTIONS:
                sqs = sqs.exclude(institution=institution)

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
