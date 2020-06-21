from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search.json/(?P<query>.+)/$', views.search),
    url(r'^search.tsv/(?P<query>.+)/$', views.search_tsv),
    url(r'^mef_captcha/$', views.mef_captcha),
]
