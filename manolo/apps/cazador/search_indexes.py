from haystack import indexes
from .models import Cazador


class CazadorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Cazador
