from haystack.forms import HighlightedSearchForm


class CazadorForm(HighlightedSearchForm):
    def search(self):
        sqs = super(CazadorForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self.searchqueryset.using('cazador').auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
