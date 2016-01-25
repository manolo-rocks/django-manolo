from django.shortcuts import render_to_response

from cazador.forms import CazadorForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    form = CazadorForm(request.GET)
    query = request.GET['q']

    all_items = form.search()
    all_items = [i.object for i in all_items]

    return render_to_response("cazador/results.html",
                  {
                      "results": all_items,
                  }
                  )
