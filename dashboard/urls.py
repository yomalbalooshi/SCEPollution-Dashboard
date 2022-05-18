from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
urlpatterns = [
    path("", views.index, name='index'),
    path('res', views.res, name='res'),
    path('doccall', views.doccall, name='doccall'),
    path('date', views.date, name='date'),

    #path('GeoJSONDataCreation', views.GeoJSONDataCreation, name='GeoJSONDataCreation'),
    #path('appendToGeoJSON', views.appendToGeoJSON, name='appendToGeoJSON'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]