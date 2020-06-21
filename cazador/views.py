import urllib

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from cazador.forms import CazadorForm
from visitors.views import do_pagination


@csrf_exempt
def index(request):
    try:
        original_query = request.GET['q']
    except:
        return render("cazador/index.html")

    all_items = []
    query_list = original_query.splitlines()
    for query in query_list:
        request_query = {'q': query}
        form = CazadorForm(request_query)
        query_results = form.search()
        all_items += query_results

    search_queryset = list(set(all_items))
    paginator, page = do_pagination(request, search_queryset)

    return render("cazador/results.html",
                  {
                      "paginator": paginator,
                      "page": page,
                      "query": "; ".join(query_list),
                      "original_query": original_query,
                      "encoded_query": urllib.parse.quote_plus(original_query.strip()),
                  }
                  )
