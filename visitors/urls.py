from django.urls import path

from visitors import views

urlpatterns = [
    path('', views.index, name='index'),
]
