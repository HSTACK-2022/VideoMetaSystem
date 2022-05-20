from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = "Core"

urlpatterns = [
    path('test/', views.home, name="home"),
    path('test/upload/', views.uploadFile, name="uploadFile"),
    path('test/upload/lists', views.uploadLists, name="uploadLists"),
    path('test/search/', views.searchFile, name="searchFile"),
    path('test/detail/<int:pk>', views.detailFile, name="detailFile"),
    path('test/success/<int:pk>', views.success, name="success"),

    path('test/minhwa', views.test_minhwa),
    path('test/minhwa2/detailSearch/', views.test_minhwa3, name="detailSearch"),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )