from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from cazador.forms import CazadorForm
from .utils import shrink_url_in_string


@csrf_exempt
def index(request):
    form = CazadorForm(request.GET)
    try:
        query = request.GET['q']
    except:
        return render_to_response("cazador/index.html")

    all_items = form.search()

    django_items = []
    for i in all_items:
        raw_data = i.object.raw_data
        i.object.raw_data = shrink_url_in_string(raw_data)
        django_items.append(i.object)

    return render_to_response("cazador/results.html",
                  {
                      "results": django_items,
                      "query": query,
                  }
                  )
