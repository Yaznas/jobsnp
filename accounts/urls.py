from django.urls import path
from .import views

urlpatterns = [
    path('signup/', views.signup, name ='signup'),
    path('signup/jobseeker', views.JobseekerSignUpView.as_view(), name='jobseeker_signup'),
    path('signup/employer', views.EmployerSignUpView.as_view(), name='employer_signup'),
]
