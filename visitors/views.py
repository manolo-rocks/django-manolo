import datetime
import csv
import logging
import re
from typing import Any, Dict
from urllib.parse import quote

from django.contrib.postgres.search import SearchQuery
from django.shortcuts import render, redirect
from django.core.paginator import PageNotAnInteger, EmptyPage, InvalidPage
from django.http import Http404, HttpResponse
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt

from visitors.models import (Visitor, Statistic, Statistic_detail, Developer, VisitorScrapeProgress,
    Institution
)
from visitors.utils import Paginator, get_sort_field


logger = logging.getLogger(__name__)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def index(request):
    context = get_context()
    stats = Statistic.objects.last()
    if stats:
        count = stats.visitor_count
    else:
        count = 0
    context['count'] = count

    if stats and stats.updated_institutions:
        institutions = stats.updated_institutions
        for institution in institutions:
            try:
                institution['last_updated'] = datetime.datetime.strptime(
                    institution['last_updated'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                institution['last_updated'] = datetime.datetime.strptime(
                    institution['last_updated'], '%Y-%m-%d')
    else:
        institutions = []
    context['institutions'] = institutions

    return render(
        request,
        "index.html",
        context=context,
    )


def about(request):
    raise Http404("This page is not available.")
    # developers = Developer.objects.all().order_by('rank')
    # context = get_user_profile(request)
    # context['developers'] = developers.exclude(project_leader=True)
    #
    # try:
    #     context['project_leader'] = Developer.objects.get(project_leader=True)
    # except Developer.DoesNotExist:
    #     context['project_leader'] = None
    #
    # return render(
    #     request,
    #     "about.html",
    #     context
    # )


def statistics(request):
    visitors = Statistic_detail.objects.all()
    visitor_counts = dict()

    for entry in VisitorScrapeProgress.objects.all().order_by('cutoff_date'):
        date_str = str(entry.cutoff_date.strftime('%Y'))
        visitor_counts[date_str] = entry.visitor_count

    context = get_context()
    context['visitors'] = visitors
    context['visitor_counts'] = list(visitor_counts.values())
    context['visitor_counts_start'] = list(visitor_counts.keys())[0]

    return render(
        request,
        "statistics.html",
        context=context,
    )


def statistics_api(request):
    try:
        stats = Statistic.objects.all()[0]
        data = stats.data
    except IndexError:
        logger.warning("Need to compute statistics")
        data = '{"error": "no data"}'
    return HttpResponse(data)


def get_context() -> Dict[str, Any]:
    return {
        "count": "",
        "full_name": "",
        'title': 'Búsqueda de Visitas | Manolo - Transparencia Gubernamental Perú',
        'meta_description': 'Busca registros de visitas a instituciones del Estado Peruano. Base de datos transparente de visitantes gubernamentales.',
    }


@csrf_exempt
def visitas(request, dni):
    context = get_context()
    query = dni.strip()

    if len(query.split()) == 1:
        single_word_query = True
    else:
        single_word_query = False

    if query_is_dni(query):
        # do dni search
        all_items = do_dni_search(query)
    else:
        if single_word_query:
            all_items = Visitor.objects.filter(
                full_search=SearchQuery(query)
            )[0:2000]
        else:
            all_items = Visitor.objects.filter(
                full_search=SearchQuery(query)
            )

    if all_items:
        full_name = all_items[0].full_name
    else:
        full_name = ""

    count = all_items.count()
    # sort queryset
    if not single_word_query:
        all_items = do_sorting(request, all_items)

    # paginate queryset
    paginator, page = do_pagination(request, all_items)

    json_path = request.get_full_path() + '&json'
    tsv_path = request.get_full_path() + '&tsv'
    encoded_query = quote(query)

    # Generate dynamic title and description
    title = f"Registros de visitas para {full_name} {query} | Manolo - Transparencia Gubernamental Perú"
    description = f"Resultados de búsqueda para el visitante {full_name} {query}. Encuentra registros detallados de visitas a instituciones gubernamentales del Perú."

    context["title"] = title
    context["meta_description"] = description
    context["count"] = count
    context["full_name"] = full_name
    context["is_visitas_dni_page"] = True
    context["paginator"] = paginator
    context["page"] = page
    context["query"] = encoded_query
    context["plain_query"] = query
    context["json_path"] = json_path
    context["tsv_path"] = tsv_path

    return render(
        request,
        "search/search.html",
        context=context,
    )


@csrf_exempt
def search(request):
    query = request.GET.get('q') or ''
    institution = request.GET.get('i') or ''

    if institution:
        try:
            institution_obj = Institution.objects.get(slug=institution)
        except Institution.DoesNotExist:
            return redirect('/')

        all_items = Visitor.objects.filter(
            institution2=institution_obj,
        ).order_by("-date")
        query = institution
    else:
        query = query.strip()

        if len(query.split()) == 1:
            single_word_query = True
        else:
            single_word_query = False

        if query_is_dni(query):
            # do dni search
            all_items = do_dni_search(query)
        else:
            if single_word_query:
                all_items = Visitor.objects.filter(
                    full_search=SearchQuery(query)
                )[0:2000]
            else:
                all_items = Visitor.objects.filter(
                    full_search=SearchQuery(query)
                )

        # sort queryset
        if not single_word_query:
            all_items = do_sorting(request, all_items)

    # paginate queryset
    paginator, page = do_pagination(request, all_items)

    json_path = request.get_full_path() + '&json'
    tsv_path = request.get_full_path() + '&tsv'
    encoded_query = quote(query)
    context = get_context()
    context["is_visitas_dni_page"] = False
    context["paginator"] = paginator
    context["page"] = page
    context["query"] = encoded_query
    context["plain_query"] = query
    context["json_path"] = json_path
    context["tsv_path"] = tsv_path

    return render(
        request,
        "search/search.html",
        context=context,
    )


def query_is_dni(query):
    if re.search(r'^(\d{5,})', query):
        return True
    else:
        return False


def do_dni_search(query):
    return Visitor.objects.filter(
        id_number=query,
    ).order_by('-date')


def search_date(request):
    context = get_context()
    if 'q' in request.GET:
        query = request.GET['q']
        if query.strip() == '':
            return redirect('/')

        try:
            query_date_obj = datetime.datetime.strptime(query, '%d/%m/%Y')
        except ValueError:
            results = "No se encontraron resultados."
            context['is_visitas_dni_page'] = False
            context['items'] = results
            context['keyword'] = query
            return render(
                request,
                "search/search.html",
                context=context,
            )
        six_months_ago = datetime.datetime.today() - datetime.timedelta(days=180)

        if query_date_obj < six_months_ago:
            can_show_results = True
        else:
            try:
                if request.user.subscriber.credits > 0:
                    can_show_results = True
                else:
                    can_show_results = False
            except AttributeError:
                # user has no subscriber
                can_show_results = False

        # TODO: implement django queryset search here
        results = []
        paginator, page = do_pagination(request, results)

        context["paginator"] = paginator
        context["query"] = query
        context["is_visitas_dni_page"] = False

        if can_show_results:
            try:
                if len(results) > 0 and request.user.subscriber:
                    if request.user.subscriber.credits is not None:
                        request.user.subscriber.credits -= 1
                        request.user.subscriber.save()
            except AttributeError:
                pass
            context["page"] = page
        else:
            context["extra_premium_results"] = len(results)
        return render(request, "search/search.html", context)
    else:
        return redirect('/')


def data_as_csv(request, paginator):
    if 'page' in request.GET:
        page = request.GET['page']
    else:
        page = ''

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        articles = paginator.page(paginator.num_pages)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="manolo_data.tsv"'

    writer = csv.writer(response, dialect='excel-tab')
    for i in articles.object_list:
        writer.writerow([i.id, i.institution, i.date, i.full_name,
                         i.id_document, i.id_number, i.entity, i.reason,
                         i.host_name, i.office, i.meeting_place,
                         i.time_start, i.time_end])
    return response


def api(request):
    return render(request, "api.html")


def do_pagination(request, all_items):
    """
    :param request: contains the current page requested by user
    :param all_items:
    :return: dict containing paginated items and pagination bar
    """
    results_per_page = 20
    results = all_items

    try:
        page_no = int(request.GET.get('page', 1))
    except (TypeError, ValueError):
        raise Http404("Not a valid number for page.")

    if page_no < 1:
        raise Http404("Pages should be 1 or greater.")

    paginator = Paginator(results, results_per_page)

    try:
        page = paginator.page(page_no)
    except InvalidPage:
        raise Http404("No such page!")

    return paginator, page


def do_sorting(request, queryset):
    ordering = get_sort_field(request)
    if not ordering:
        return queryset.order_by('-date')
    return queryset.order_by(ordering)


def ads_txt_view(request):
    content = "google.com, pub-5536287228450200, DIRECT, f08c47fec0942fa0"
    return HttpResponse(content, content_type="text/plain")

