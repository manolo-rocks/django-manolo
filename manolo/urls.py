# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from visitors import views


urlpatterns = patterns(
    '',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search_date/$', views.search_date),
    url(r'^search/', views.search, name='search_view'),
    url(r'^api/', views.api, name='api'),
    # url(r'^search/', include('haystack.urls')),
    url(r'^$', include('visitors.urls', namespace="visitors")),
    url(r'robots.txt$', views.robots, name='robots'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# TODO: rewrite build_page method of haystack.views SearchView to
# produce a nicer pagination that includes max 20 pages to click
