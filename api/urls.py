from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search.json/(?P<query>.+)/$', views.search, name='search-json'),
    url(r'^search.tsv/(?P<query>.+)/$', views.search_tsv, name='search-tsv'),
    url(r'^mef_captcha/$', views.mef_captcha, name='mef-captcha'),
]
