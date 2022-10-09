from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search.json/(?P<query>.+)/$', views.search, name='search-json'),
    url(r'^search.tsv/(?P<query>.+)/$', views.search_tsv, name='search-tsv'),
    url(r'^mef_captcha/$', views.mef_captcha, name='mef-captcha'),
    url(r'^save_file/$', views.save_file, name='save-file'),
    url(r'^save_json/$', views.save_json, name='save-json'),
    url(r'^count_visits/(?P<dni_number>.+)$', views.count_visits, name='count-visits'),
]
