import json
import os
import subprocess
import time
from datetime import datetime
from uuid import uuid4

from django.http.request import QueryDict
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
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
from visitors.views import do_pagination, data_as_csv, do_sorting, sanitize_query
from .tasks import process_json_request, log_task_error


schema_view = get_schema_view(
    openapi.Info(
        title="Manolo API",
        description="Documentación del API de Manolo.rocks",
        default_version="v1",
        contact=openapi.Contact(email="mycalesis@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


@api_view(["GET"])
@permission_classes((AllowAny,))
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
        description: nombre o palabra clave a buscar, por ejemplo Romulo
        type: string
        paramType: path
        required: true
    """
    try:
        query = sanitize_query(query)
    except Exception as e:
        return HttpResponse(f"Invalid request: {e}", status=400)

    query_request = QueryDict("q={}".format(query))
    form = ApiForm(query_request)
    all_items = form.search()

    # sort queryset
    all_items = do_sorting(request, all_items)

    pagination = PageNumberPagination()
    paginated_results = pagination.paginate_queryset(all_items, request)

    serializer = ManoloSerializer(paginated_results, many=True)

    data = {
        "count": pagination.page.paginator.count,
        "next": pagination.get_next_link(),
        "previous": pagination.get_previous_link(),
        "results": serializer.data,
    }
    return JSONResponse(data)


@api_view(["GET"])
@permission_classes((AllowAny,))
def search_tsv(request, query):
    try:
        query = sanitize_query(query)
    except Exception as e:
        return HttpResponse(f"Invalid request: {e}", status=400)

    query_request = QueryDict("q={}".format(query))
    form = ApiForm(query_request)
    all_items = form.search()

    # sort queryset
    all_items = do_sorting(request, all_items)
    # paginate queryset
    paginator, page = do_pagination(request, all_items)

    return data_as_csv(request, paginator)


@csrf_exempt
@api_view(["POST"])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAdminUser,))
def mef_captcha(request):
    """Accepts a CAPTCHA image from MEF and returns the text

    Usage:

    import requests
    from requests.auth import HTTPBasicAuth

    fin = open("images/image_10.jpg", "rb")
    files = {'file': fin}
    url = "https://manolo.rocks/api/mef_captcha/"

    auth = HTTPBasicAuth("user", "pass")
    res = requests.post(url, files=files, auth=auth)
    print(res.text)
    """
    if "file" in request.FILES:
        myfile = request.FILES["file"]
        text = ocr_image(myfile.read())
        return HttpResponse(text)
    return "hi there"


def ocr_image(file_content):
    filename = "/tmp/" + str(uuid4()) + ".jpg"

    with open(filename, "wb") as handle:
        handle.write(file_content)

    basename = filename.replace(".jpg", "").replace("/tmp/", "")

    # process
    black_white_image_filename = "/tmp/{}-1.jpg".format(basename)
    cmd = "convert {} -threshold 90% {}".format(filename, black_white_image_filename)
    subprocess.call(cmd, shell=True)

    cmd = "tesseract -psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNPQRSTUVWXYabcdefghijkmnpqrstuvwxy23456789 {} {}".format(  # noqa
        black_white_image_filename, basename
    )
    subprocess.call(cmd, shell=True)
    with open("{}.txt".format(basename), "r") as handle:
        text = handle.read().strip().replace(" ", "")
    os.remove("{}.txt".format(basename))
    return text


@api_view(["POST"])
@permission_classes((HasAPIKey,))
def save_file(request):
    """Receive a jsonlines file of scraped data to be stored in the database"""
    if is_key_valid(request) is False:
        return HttpResponse("bad key")

    binary_data = request.FILES["file"].read()
    data = binary_data.decode().splitlines()

    for line in data:
        item = json.loads(line)
        process_item(item)

    return HttpResponse("ok")


@api_view(["POST"])
@permission_classes((HasAPIKey,))
def save_json_single_inst(request):
    """Save a json file of scraped data from a single institution

    Download is done month by month on a single institution basis
    """
    if is_key_valid(request) is False:
        return HttpResponse("bad key")

    institution_name = request.FILES["file"].name.replace(".json", "")

    if "visitas_gob_pe_" in institution_name:
        institution_ruc = institution_name.split("_")[3]
    else:
        raise ValueError(
            "Institution name does not match expected format: "
            "'visitas_gob_pe_<institution_ruc>.json'"
        )

    binary_data = request.FILES["file"].read()
    data = json.loads(binary_data.decode())

    for item in data:
        item["institution_ruc"] = institution_ruc
        item["date"] = datetime.strptime(item["fecha"], "%d/%m/%Y").strftime("%Y-%m-%d")
        item["id_document"] = item["documento"].split()[0]
        item["id_number"] = " ".join(item["documento"].split()[1:]).strip()
        item["host_name"] = item["funcionario"]
        item["full_name"] = item["visitante"]
        item["time_start"] = item["horaIn"]
        item["time_end"] = item["horaOut"]
        item["reason"] = item.get("motivo", "")
        item["entity"] = item["rz_empresa"]
        item["location"] = item.get("no_lugar_r", "").split(" - ")[0]
        item["meeting_place"] = " ".join(item.get("no_lugar_r", "").split(" - ")[1:]).strip()

    task = process_json_request.s(data)
    task.apply_async(link_error=log_task_error.s(institution_name))

    return HttpResponse("ok")


@api_view(["POST"])
@permission_classes((HasAPIKey,))
def save_json(request):
    """Receive a json file of scraped data to be stored in the database"""
    if is_key_valid(request) is False:
        return HttpResponse("bad key")

    institution_name = request.FILES["file"].name.replace(".json", "")
    binary_data = request.FILES["file"].read()
    data = binary_data.decode().splitlines()

    task = process_json_request.s(data)
    task.apply_async(link_error=log_task_error.s(institution_name))

    return HttpResponse("ok")


@permission_classes((HasAPIKey,))
def count_visits(request, dni_number):
    try:
        dni_number = sanitize_query(dni_number)
    except Exception as e:
        return HttpResponse(f"Invalid request: {e}", status=400)

    if is_key_valid(request) is False:
        return HttpResponse("bad key", status=400)

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
