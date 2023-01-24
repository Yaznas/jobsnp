from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path('', views.home, name='home'),
    path('post-job/', views.post_job_view, name='post-job'),
    path('update-job/<int:id>', views.update_job_view, name='update-job'),
    path('delete-job/<int:id>', views.delete_job_view, name='delete-job'),
    path('jobs-list', views.jobs_list_view, name='jobs-list'),
    path('job/<int:id>/', views.job_detail_view, name='job-detail'),
    path('apply-job/<int:id>/', views.apply_job_view, name='apply-job'),
    path('bookmark-job/<int:id>/', views.job_bookmark_view, name='bookmark-job'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/employer/job/<int:id>/applicants/', views.all_applicants_view, name='applicants'),
    path('dashboard/employer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('dashboard/employer/close/<int:id>/', views.make_complete_job_view, name='complete'),
    path('dashboard/jobseeker/delete-bookmark/<int:id>/', views.delete_bookmark_view, name='delete-bookmark'),
     path('result/', views.search_job_view, name='search-job'),
]