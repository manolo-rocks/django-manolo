from django.urls import path

from . import views

urlpatterns = [
    # path('search.json/<path:query>/', views.search, name='search-json'),
    # path('search.tsv/<path:query>/', views.search_tsv, name='search-tsv'),
    # path('mef_captcha/', views.mef_captcha, name='mef-captcha'),
    path("save_file/", views.save_file, name="save-file"),
    path("save_json/", views.save_json, name="save-json"),
    path("save_json_single_inst/", views.save_json_single_inst, name="save-json_single-inst"),
    path("count_visits/<str:dni_number>", views.count_visits, name="count-visits"),
]
