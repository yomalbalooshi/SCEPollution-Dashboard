from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name='index'),
    path('qu', views.qu, name="qu"),
   path('res', views.res, name='res'),
    path('url', views.url, name='url')
   # path('generateEmbedUrlForAnonymousUser', views.generateEmbedUrlForAnonymousUser, name='generateEmbedUrlForAnonymousUser')
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

