import json
import time

from django.http.request import QueryDict
from django.shortcuts import HttpResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from scrapers.manolo_scraper.pipelines import process_item
from visitors.models import Visitor
from .forms import ApiForm
from .serializers import ManoloSerializer
from .api_responses import JSONResponse
from visitors.views import do_pagination, data_as_csv, do_sorting
from .tasks import process_json_request, log_task_error


schema_view = get_schema_view(
    openapi.Info(
        title="Manolo API",
        description='Documentación del API de Manolo.rocks',
        default_version='v1',
        contact=openapi.Contact(email='mycalesis@gmail.com'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
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
    all_items = form.search()

    # sort queryset
    all_items = do_sorting(request, all_items)

    pagination = PageNumberPagination()
    paginated_results = pagination.paginate_queryset(all_items, request)

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
    all_items = form.search()

    # sort queryset
    all_items = do_sorting(request, all_items)
    # paginate queryset
    paginator, page = do_pagination(request, all_items)

    return data_as_csv(request, paginator)


@api_view(['POST'])
@permission_classes((HasAPIKey, ))
def save_file(request):
    """Receive a jsonlines file of scraped data to be stored in the database"""
    if is_key_valid(request) is False:
        return HttpResponse("bad key")

    binary_data = request.FILES['file'].read()
    data = binary_data.decode().splitlines()

    for line in data:
        item = json.loads(line)
        process_item(item)

    return HttpResponse('ok')


@api_view(['POST'])
@permission_classes((HasAPIKey, ))
def save_json(request):
    """Receive a json file of scraped data to be stored in the database"""
    if is_key_valid(request) is False:
        return HttpResponse("bad key")

    name = request.FILES["file"].name.replace(".json", "")
    binary_data = request.FILES['file'].read()
    data = binary_data.decode().splitlines()

    task = process_json_request.s(data, institution_name=name)
    task.apply_async(link_error=log_task_error.s(name))

    return HttpResponse('ok')


@permission_classes((HasAPIKey,))
def count_visits(request, dni_number):
    if is_key_valid(request) is False:
        return HttpResponse("bad key")

    count = Visitor.objects.filter(id_number=dni_number).count()
    return HttpResponse(count)


def is_key_valid(request):
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
    except (KeyError, IndexError):
        time.sleep(30)
        return False

    try:
        APIKey.objects.get_from_key(key)
    except APIKey.DoesNotExist:
        time.sleep(30)
        return False

    return True
