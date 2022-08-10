from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name ='signup'),
    path('signup/jobseeker/', views.JobseekerSignUpView.as_view(), name='jobseeker_signup'),
    path('signup/employer/', views.EmployerSignUpView.as_view(), name='employer_signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name= "logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
