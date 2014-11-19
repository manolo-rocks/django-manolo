import datetime
import re

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from manolo.models import Manolo


def index(request):
    return render(request, "manolo/index.html")


def search(request):
    template = loader.get_template('manolo/search_result.html')
    if 'q' in request.GET:
        query = request.GET['q']
        if query.strip() == '':
            return redirect('/manolo/')
        else:
            results = find_in_db(query)

        if results == "No se encontraron resultados.":
            return render(request,
                          "manolo/search_result.html",
                          {'items': results, 'keyword': query, }
                          )
        else:
            all_items = results
            obj = do_pagination(request, all_items)
            return render(request, "manolo/search_result.html",
                          {
                              "items": obj['items'],
                              "first_half": obj['first_half'],
                              "second_half": obj['second_half'],
                              "first_page": obj['first_page'],
                              "last_page": obj['last_page'],
                              "current": obj['current'],
                              "pagination_keyword": query,
                              "keyword": query,
                          }
                          )
    else:
        return redirect('/manolo/')


def validate(query):
    try:
        return datetime.datetime.strptime(query, "%d/%m/%Y")
    except ValueError:
        return False


def sanitize(s):
    s = s.replace("'", "")
    s = s.replace('"', "")
    s = s.replace("/", "")
    s = s.replace("\\", "")
    s = s.replace(";", "")
    s = s.replace("=", "")
    s = s.replace("*", "")
    s = s.replace("%", "")
    new_s = s.strip()
    new_s = re.sub("\s+", " ", new_s)
    return new_s


def find_in_db(query):
    """
    Finds items according to user search.

    :param query: user's keyword
    :return: QuerySet object with items or string if no results were found.
    """
    # find if it is date
    it_is_date = validate(query)
    if it_is_date is not False:
        results = Manolo.objects.filter(date=it_is_date)
    else:
        query = sanitize(query)
        try:
            results = Manolo.objects.filter(
                Q(visitor__icontains=query) |
                Q(id_document__icontains=query) |
                Q(entity__icontains=query) |
                Q(objective__icontains=query) |
                Q(host__icontains=query) |
                Q(office__icontains=query) |
                Q(meeting_place__icontains=query),
            ).order_by('-date')
        except Manolo.DoesNotExist:
            results = "No se encontraron resultados."
    # count number of results
    # return list of entries for template
    if len(results) < 1:
        return "No se encontraron resultados."
    else:
        return results


def do_pagination(request, all_items):
    """
    :param request: contains the current page requested by user
    :param all_items:
    :return: dict containing paginated items and pagination bar
    """
    paginator = Paginator(all_items, 50)

    page = request.GET.get('page')

    try:
        items = paginator.page(page)
        cur = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
        cur = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)
        cur = 1

    if cur > 20:
        first_half = range(cur - 10, cur)
        # is current less than last page?
        if cur < paginator.page_range[-1] - 10:
            second_half = range(cur + 1, cur + 10)
        else:
            second_half = range(cur + 1, paginator.page_range[-1])
    else:
        first_half = range(1, cur)
        if paginator.page_range[-1] > 20:
            second_half = range(cur + 1, 21)
        else:
            second_half = range(cur + 1, paginator.page_range[-1] + 1)

    obj = {
        'items': items,
        "first_half": first_half,
        "second_half": second_half,
        "first_page": paginator.page_range[0],
        "last_page": paginator.page_range[-1],
        "current": cur,
    }
    return obj
