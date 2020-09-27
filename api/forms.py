from django.forms import Form

from visitors.models import Visitor


class ApiForm(Form):
    def search(self):
        if not self.is_valid():
            return None

        query = self.data['q'].strip()
        if not query:
            return None

        return Visitor.objects.filter(
            full_name__icontains=query
        ).order_by('-date')
