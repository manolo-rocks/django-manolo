from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^search.json/(?P<query>.+)/$', views.search),
)
