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

    path('test/success/', views.success, name="success"),

    path('test/minhwa', views.test_minhwa),
<<<<<<< HEAD
    path('test/minhwa2/detailSearch/', views.test_minhwa3, name="detailSearch"),
=======
    #path('test/minhwa2/', views.test_minhwa2, name="minhwa"),
    path('test/minhwa2/detailSearch/', views.test_minhwa3, name="detailSearch"),
    #path('test/success/finish/', views.test_successFinish, name="uploadFinish"),
>>>>>>> ef7b06d7f03380ea86b491bd6d823e363325972c
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )