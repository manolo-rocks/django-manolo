from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

from visitors import views
from visitors.views import ads_txt_view

admin.autodiscover()


urlpatterns = [
    path('administramelo/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
    path('search_date/', views.search_date),
    path('search/', views.search, name='search_view'),
    path('visitas/<path:dni>/', views.visitas, name='visitas'),
    path('api/', include('api.urls')),
    # path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('statistics/', views.statistics, name='statistics'),
    path('statistics_api/', views.statistics_api),
    path('ads.txt', ads_txt_view),

    path('about/', views.about, name='about'),
    path('', include('visitors.urls')),
    path('cazador/', include('cazador.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
