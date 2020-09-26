import datetime

from django.forms import Form

from visitors.models import Visitor


class ApiForm(Form):
    def search(self):
        if not self.is_valid():
            return None

        query = self.data['q'].strip()
        if not query:
            return None

        visitors = Visitor.objects.filter(full_name__icontains=query).order_by('-date')
        today = datetime.datetime.today()
        six_months_ago = today - datetime.timedelta(days=180)
        visitors = visitors.filter(date__lte=six_months_ago)

        return visitors
