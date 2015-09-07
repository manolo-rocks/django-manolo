from django.shortcuts import render
from django.http.request import QueryDict

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from .forms import ApiForm


@api_view(['GET'])
@permission_classes((AllowAny, ))
def search(request, query):
    query_request = QueryDict('q={}'.format(query))
    print(">>>>>>>request_copy", query_request)
    form = ApiForm(query_request)

    return render(request, "search/search.html")
