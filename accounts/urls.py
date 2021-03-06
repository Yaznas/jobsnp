from django.contrib import admin
from django.urls import path, include
from accounts import views as user_views
from django.contrib.auth import views as authentication_views

urlpatterns = [
    path('register/',user_views.register, name='register'),
    path('login/',authentication_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/',authentication_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profilepage, name='profile'),
]
