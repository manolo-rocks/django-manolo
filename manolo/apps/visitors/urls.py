from django.conf.urls import patterns, include, url

from visitors import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
