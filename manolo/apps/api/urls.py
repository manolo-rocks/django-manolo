from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^search.json/(?P<query>.+)/$', views.search),
    url(r'^search.tsv/(?P<query>.+)/$', views.search_tsv),
)
