from django import forms
from haystack.forms import SearchForm


class ApiForm(SearchForm):
    def search(self):
        sqs = super(ApiForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data['q'].strip():
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data['q']).order_by('-date')

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
