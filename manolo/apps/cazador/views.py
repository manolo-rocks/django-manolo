import urllib

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from manolo.apps.cazador.forms import CazadorForm
from manolo.apps.visitors.views import do_pagination


@csrf_exempt
def index(request):
    try:
        original_query = request.GET['q']
    except:
        return render_to_response("cazador/index.html")

    all_items = []
    query_list = original_query.splitlines()
    for query in query_list:
        request_query = {'q': query}
        form = CazadorForm(request_query)
        query_results = form.search()
        all_items += query_results

    search_queryset = list(set(all_items))
    paginator, page = do_pagination(request, search_queryset)

    return render_to_response("cazador/results.html",
                  {
                      "paginator": paginator,
                      "page": page,
                      "query": urllib.parse.quote_plus(original_query),
                  }
                  )
