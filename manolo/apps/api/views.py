from django.shortcuts import render
from django.http.request import QueryDict

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from .forms import ApiForm
from .serializers import ManoloSerializer


@api_view(['GET'])
@permission_classes((AllowAny, ))
def search(request, query):
    query_request = QueryDict('q={}'.format(query))
    form = ApiForm(query_request)
    results = [i.object for i in form.search()]
    serializer = ManoloSerializer(results, many=True)
    print(serializer.data)

    return render(request, "search/search.html")
