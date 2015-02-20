from haystack.forms import HighlightedSearchForm


class ManoloForm(HighlightedSearchForm):
    def search(self):
        return super(ManoloForm, self).search()
