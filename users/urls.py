from django.contrib.auth import views as auth_views
from django.urls import path


from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/following/', views.following, name='following'),
    path('profile/update/', views.profile_update, name='profile_update')
]
