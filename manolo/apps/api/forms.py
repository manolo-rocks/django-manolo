from django import forms
from haystack.forms import SearchForm


class ApiForm(SearchForm):
    query = forms.CharField()

    def search(self):
        sqs = super(ApiForm, self).search()
        print(">>>> is valid?", self.is_valid())
        print(">>>> clenaded data?", self.cleaned_data)

        if not self.is_valid():
            return self.no_query_found()

        return sqs
