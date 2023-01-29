from django.urls import path
from . import views
from createresume.views import ResumeListView

app_name = "createresume"

urlpatterns = [
    path("resume-form/", views.create_resume_view, name="resume-form"),
    path("resume/<int:id>/", views.resume_detail_view, name="resume"),
    path("", ResumeListView.as_view(), name="resume-list"),
]
