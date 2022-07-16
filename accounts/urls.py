from django.contrib import admin
from django.urls import path, include
from accounts import views as user_views

urlpatterns = [
    path('register/',user_views.register, name='register'),
]
