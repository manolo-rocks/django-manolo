# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from drf_yasg.views import get_schema_view

admin.autodiscover()

from visitors import views
from api.views import schema_view


urlpatterns = [
    path('administramelo/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^search_date/$', views.search_date),
    url(r'^search/', views.search, name='search_view'),
    url(r'^api/', include('api.urls')),
    url(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redocs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^statistics/$', views.statistics),
    url(r'^statistics_api/$', views.statistics_api),

    url(r'^about/', views.about, name='about'),
    path('', include('visitors.urls')),
    path('robots.txt', views.robots_txt, name='robots'),
    url(r'^cazador/', include('cazador.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
