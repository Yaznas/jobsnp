from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post-job/', views.post_job_view, name='post-job'),
    path('update/<int:job_id>', views.job_update_view, name='update-job'),
    path('delete/<int:job_id>', views.job_delete_view, name='delete-job'),
]