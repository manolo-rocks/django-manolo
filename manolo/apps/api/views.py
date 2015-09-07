from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes((AllowAny, ))
def search(request, query):
    print(query)
