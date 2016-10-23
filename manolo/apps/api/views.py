# -*- coding: utf-8 -*-
from django.http.request import QueryDict

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework import response, schemas

from .forms import ApiForm
from .serializers import ManoloSerializer
from .api_responses import JSONResponse
from visitors.views import do_pagination, data_as_csv


@api_view()
@permission_classes((AllowAny, ))
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Documentación del API de Manolo.')
    return response.Response(
        generator.get_schema(request=request),
    )


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
    if request.user.is_authenticated():
        all_items = form.search(premium=True)
    else:
        all_items = form.search(premium=False)

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


@api_view(['GET'])
@permission_classes((AllowAny, ))
def search_tsv(request, query):
    query_request = QueryDict('q={}'.format(query))
    form = ApiForm(query_request)
    if request.user.is_authenticated():
        all_items = form.search(premium=True)
    else:
        all_items = form.search(premium=False)

    paginator, page = do_pagination(request, all_items)
    return data_as_csv(request, paginator)
