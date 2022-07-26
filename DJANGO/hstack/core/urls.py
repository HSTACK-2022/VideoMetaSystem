from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = "Core"

urlpatterns = [
    path('', views.home, name="home"),
    path('upload/', views.uploadFile, name="uploadFile"),
    path('upload/lists', views.uploadLists, name="uploadLists"),
    path('search/', views.searchFile, name="searchFile"),
    path('detail/<int:pk>', views.detailFile, name="detailFile"),
    path('success/<int:pk>', views.success, name="success"),
    path('search/detailSearch/', views.detailSearch, name="detailSearch"),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )