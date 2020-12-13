from django.contrib.postgres.search import SearchQuery
from django.forms import Form

from visitors.models import Visitor
from visitors.views import query_is_dni, do_dni_search


class ApiForm(Form):
    def search(self):
        if not self.is_valid():
            return None

        query = self.data['q'].strip()
        if not query:
            return None

        if query_is_dni(query):
            return do_dni_search(query)
        else:
            return Visitor.objects.filter(
                full_search=SearchQuery(query)
            )
