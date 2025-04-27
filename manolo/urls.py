from django.conf import settings
from django.http import HttpResponse
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

from api.views import schema_view
from visitors import views


admin.autodiscover()


def ads_txt_view(request):
    content = "google.com, pub-5536287228450200, DIRECT, f08c47fec0942fa0"
    return HttpResponse(content, content_type="text/plain")



urlpatterns = [
    path('administramelo/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
    path('search_date/', views.search_date),
    path('search/', views.search, name='search_view'),
    path('api/', include('api.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('statistics/', views.statistics, name='statistics'),
    path('statistics_api/', views.statistics_api),

    path('about/', views.about, name='about'),
    path('', include('visitors.urls')),
    path('cazador/', include('cazador.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
