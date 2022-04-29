from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
app_name = "Core"

urlpatterns = [
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('core/create_post/', views.PostCreate.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
<<<<<<< Updated upstream
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'),views.PostList.as_view(), name='login'),
=======
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('signup/',views.signup, name="signup")
>>>>>>> Stashed changes
    #path('/upload/', views.uploadFile, name="uploadFile"),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )