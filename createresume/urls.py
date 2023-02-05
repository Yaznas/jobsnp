from django.urls import path
from . import views

app_name = "createresume"

urlpatterns = [
    path("resume-form/", views.create_resume_view, name="resume-form"),
    path("resume/<int:id>/", views.resume_detail_view, name="resume"),
    path("resume/upload/", views.extract_pdf_text, name="upload-pdf"),
    path("resume/text/", views.extract_pdf_text, name="pdf-text"),
]
