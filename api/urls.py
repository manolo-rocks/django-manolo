from django.urls import path

from . import views

urlpatterns = [
    path('search.json/<str:query>/', views.search, name='search-json'),
    path('search.tsv/<str:query>/', views.search_tsv, name='search-tsv'),
    path('save_file/', views.save_file, name='save-file'),
    path('save_json/', views.save_json, name='save-json'),
    path('count_visits/<str:dni_number>', views.count_visits, name='count-visits'),
]
