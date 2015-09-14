from django.http.request import QueryDict

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from .forms import ApiForm
from .serializers import ManoloSerializer
from .api_responses import JSONResponse
from visitors.views import do_pagination, data_as_csv


@api_view(['GET'])
@permission_classes((AllowAny, ))
def search(request, query):
    """
    Lista resultados de búsqueda de palabra clave. Usa paginación y muestra
    hasta 20 resultados por página.
    Además muestra links para páginas previas y siguientes.

    # Puedes obtener los resultados en archivo TSV

    Este archivo contiene la información en campos separados por tabs
    (fácil de importar a MS Excel)

    Solo es necesario usar la dirección `search.tsv`:

    * <http://manolo.rocks/api/search.tsv/romulo/>
    ---
    type:
      query:
        required: true
        type: string
    parameters:
      - name: query
        description: nombre o palabra clave a busar, por ejemplo Romulo
        type: string
        paramType: path
        required: true
    """
    query_request = QueryDict('q={}'.format(query))
    form = ApiForm(query_request)
    all_items = form.search()

    pagination = PageNumberPagination()
    paginated_results = pagination.paginate_queryset(all_items, request)
    paginated_results = [i.object for i in paginated_results]

    serializer = ManoloSerializer(paginated_results, many=True)

    data = {
        'count': pagination.page.paginator.count,
        'next': pagination.get_next_link(),
        'previous': pagination.get_previous_link(),
        'results': serializer.data,
    }
    return JSONResponse(data)


@permission_classes((AllowAny, ))
def search_tsv(request, query):
    query_request = QueryDict('q={}'.format(query))
    form = ApiForm(query_request)
    results = form.search()

    paginator, page = do_pagination(request, results)
    return data_as_csv(request, paginator)
