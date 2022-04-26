from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "Core"

urlpatterns = [
    path('create_post/', views.PostCreate.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('upload/', views.uploadFile, name="uploadFile"),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )