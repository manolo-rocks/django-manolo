from django.conf.urls import url

from visitors import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
