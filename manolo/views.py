import datetime

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Q

from manolo.models import Manolo


def index(request):
    template = loader.get_template('manolo/index.html')
    context = RequestContext(request, {
        'intro_msg': 'hola',
    })
    return HttpResponse(template.render(context))


def search(request):
    template = loader.get_template('manolo/search_result.html')
    if 'q' in request.GET:
        query = request.GET['q']
        if query.strip() == '':
            context = RequestContext(request, {
                'items': ''
            })
            return HttpResponse(template.render(context))
        else:
            results = find_in_db(query)
            context = RequestContext(request, {
                'items': results,
                'keyword': query,
            })
            return HttpResponse(template.render(context))
    else:
        message = "you submitted and empty form."
    context = RequestContext(request, {
        'content': message,
        'keyword': query,
    })
    return HttpResponse(template.render(context))


def validate(query):
    try:
        return datetime.datetime.strptime(query, "%d/%m/%Y")
    except ValueError:
        return False


def find_in_db(query):
    # find if query is date and convert
    # connect db
    it_is_date = validate(query)
    if it_is_date is not False:
        results = Manolo.objects.filter(date=it_is_date)
    else:
        try:
            results = Manolo.objects.filter(
                Q(visitor__icontains=query) |
                Q(id_document__icontains=query) |
                Q(entity__icontains=query) |
                Q(objective__icontains=query) |
                Q(host__icontains=query) |
                Q(office__icontains=query) |
                Q(meeting_place__icontains=query),
            )
        except Manolo.DoesNotExist:
            results = "No se encontraron resultados."
    # count number of results
    # return list of entries for template
    return results
