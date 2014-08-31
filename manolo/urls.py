from django.conf.urls import patterns, url

from manolo import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search?q=(?P<query>.+)$', views.search, name='search'),
)
