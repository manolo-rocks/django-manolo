import datetime

from haystack.forms import SearchForm


class ApiForm(SearchForm):
    def search(self, premium):
        sqs = super(ApiForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data['q'].strip():
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data['q']).order_by('-date')
        if not premium:
            today = datetime.datetime.today()
            six_months_ago = today - datetime.timedelta(days=180)
            sqs = sqs.filter(date__lte=six_months_ago)

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
