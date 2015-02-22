import datetime

from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator, PageNotAnInteger
from django.core.paginator import InvalidPage
from django.http import Http404
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from haystack.query import SearchQuerySet
from django.views.decorators.csrf import csrf_exempt

from visitors.models import Visitor
from visitors.forms import ManoloForm
from visitors.serializer import VisitorSerializer
from visitors.serializer import PaginatedVisitorSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def index(request):
    return render(request, "index.html")


@csrf_exempt
def search(request):
    form = ManoloForm(request.GET)
    query = request.GET['q']

    all_items = form.search()
    paginator, page = do_pagination(request, all_items)

    if 'json' in request.GET:
        # simplified filtering of an SQS
        if 'page' in request.GET:
            page = request.GET['page']
        else:
            page = ''

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page
            articles = paginator.page(1)
        except PageNotAnInteger:
            # If page is out of range, deliver last page
            articles = paginator.page(paginator.num_pages)

        items = [i.object for i in articles]
        print(len(items))
        serializer_context = {'request': request}
        serializer = VisitorSerializer(items, context=serializer_context, many=True)
        return JSONResponse(serializer.data)

    return render(request, "search/search.html",
                  {
                      "paginator": paginator,
                      "page": page,
                      "query": query,
                  }
                  )


def search_date(request):
    if 'q' in request.GET:
        query = request.GET['q']
        if query.strip() == '':
            return redirect('/')

        try:
            date_obj = datetime.datetime.strptime(query, '%d/%m/%Y').date()
        except ValueError:
            results = "No se encontraron resultados."
            return render(
                request,
                "search/search.html",
                {'items': results, 'keyword': query, }
            )

        date_str = datetime.datetime.strftime(date_obj, '%Y-%m-%d')
        results = SearchQuerySet().filter(date=date_str)

        all_items = results
        paginator, page = do_pagination(request, all_items)
        return render(request, "search/search.html",
                      {
                          "paginator": paginator,
                          "page": page,
                          "query": query,
                      }
                      )
    else:
        return redirect('/')


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
