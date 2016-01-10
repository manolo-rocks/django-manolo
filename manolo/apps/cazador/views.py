from django.shortcuts import render_to_response, redirect
from utils import search

def index(request):
    if 'q' in request.GET:
        name = request.GET['q'].strip()
        results = search(name)

        return render_to_response('cazador/results.html', {'results': results})

    return render_to_response('cazador/index.html')

