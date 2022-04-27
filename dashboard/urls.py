from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name='index'),
    path('test', views.test, name="test"),
    path('res', views.res, name='res'),
    #path('doccall', views.doccall, name='doccall'),
    #path('GeoJSONDataCreation', views.GeoJSONDataCreation, name='GeoJSONDataCreation'),
    #path('appendToGeoJSON', views.appendToGeoJSON, name='appendToGeoJSON'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

