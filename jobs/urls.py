from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path('', views.home, name='home'),
    path('post-job/', views.post_job_view, name='post-job'),
    path('update/<int:job_id>', views.update_job_view, name='update-job'),
    path('delete/<int:job_id>', views.delete_job_view, name='delete-job'),
    path('jobs-list', views.jobs_list_view, name='jobs-list'),
    path('job/<int:id>/', views.job_detail_view, name='job-detail'),
]