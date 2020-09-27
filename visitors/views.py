import datetime
import csv
import logging

from django.db import connection
from django.shortcuts import render, redirect
from django.core.paginator import PageNotAnInteger, EmptyPage, InvalidPage
from django.http import Http404, HttpResponse
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt

from visitors.models import Visitor, Statistic, Statistic_detail
from visitors.utils import Paginator, get_user_profile


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
    user_profile = get_user_profile(request)
    count = Visitor.objects.count()
    return render(
        request,
        "index.html",
        {
            'count': count,
            'user_profile': user_profile,
        },
    )


def about(request):
    user_profile = get_user_profile(request)
    return render(
        request,
        "about.html",
        {'user_profile': user_profile},
    )


def statistics(request):
    user_profile = get_user_profile(request)
    visitors = Statistic_detail.objects.all()
    return render(
        request,
        "statistics.html",
        {
            'user_profile': user_profile,
            'visitors': visitors,
        },
    )


def statistics_api(request):
    try:
        stats = Statistic.objects.all()[0]
        data = stats.data
    except IndexError:
        logger.warning("Need to compute statistics")
        data = '{"error": "no data"}'
    return HttpResponse(data)


@csrf_exempt
def search(request):
    user_profile = get_user_profile(request)
    query = request.GET.get('q')

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT full_name, entity, meeting_place, office, "
            "host_name, reason, institution, location, "
            "id_document, id_number, date, time_start, "
            "time_end, reason, host_title FROM visitors_visitor "
            "WHERE full_name_dni @@ plainto_tsquery(%s)", [query]
        )
        all_items = cursor.fetchall()

    paginator, page = do_pagination(request, all_items)

    json_path = request.get_full_path() + '&json'
    tsv_path = request.get_full_path() + '&tsv'
    return render(
        request,
        "search/search.html",
        {
            "paginator": paginator,
            "page": page,
            "query": query,
            "json_path": json_path,
            "tsv_path": tsv_path,
            'user_profile': user_profile,
        },
    )


def search_date(request):
    user_profile = get_user_profile(request)
    if 'q' in request.GET:
        query = request.GET['q']
        if query.strip() == '':
            return redirect('/')

        try:
            query_date_obj = datetime.datetime.strptime(query, '%d/%m/%Y')
        except ValueError:
            results = "No se encontraron resultados."
            return render(
                request,
                "search/search.html",
                {
                    'items': results,
                    'keyword': query,
                    'user_profile': user_profile,
                },
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

        date_str = datetime.datetime.strftime(query_date_obj, '%Y-%m-%d')
        # TODO: implement django queryset search here
        results = []
        paginator, page = do_pagination(request, results)

        context = {
            "paginator": paginator,
            "query": query,
            'user_profile': user_profile,
        }

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

    items = [i.object for i in articles]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="manolo_data.csv"'

    writer = csv.writer(response, dialect='excel-tab')
    for i in items:
        writer.writerow([i.id, i.institution, i.date, i.full_name,
                         i.id_document, i.id_number, i.entity, i.reason,
                         i.host_name, i.office, i.meeting_place,
                         i.time_start, i.time_end])
    return response


def api(request):
    return render(request, "api.html")


def robots(request):
    return render(request, "robots.txt")


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
