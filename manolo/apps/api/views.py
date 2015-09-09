from django.http.request import QueryDict

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import renderer_classes

from .forms import ApiForm
from .serializers import ManoloSerializer
from .api_responses import CSVResponse
from .api_responses import CSVRenderer
from .api_responses import JSONResponse
from visitors.views import do_pagination, data_as_csv


@api_view(['GET'])
@permission_classes((AllowAny, ))
def search(request, query):
    query_request = QueryDict('q={}'.format(query))
    form = ApiForm(query_request)
    results = [i.object for i in form.search()]
    serializer = ManoloSerializer(results, many=True)

    pagination = PageNumberPagination()
    results = pagination.paginate_queryset(serializer.data, request)

    data = {
        'count': pagination.page.paginator.count,
        'next': pagination.get_next_link(),
        'previous': pagination.get_previous_link(),
        'results': results,
    }
    return JSONResponse(data)


@permission_classes((AllowAny, ))
@renderer_classes((CSVRenderer,))
def search_csv(request, query):
    query_request = QueryDict('q={}'.format(query))
    form = ApiForm(query_request)
    results = form.search()

    paginator, page = do_pagination(request, results)
    return data_as_csv(request, paginator)
