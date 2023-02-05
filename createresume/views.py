from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from PyPDF2 import PdfReader

from accounts.models import User
from .models import Resume
from .forms import ResumeForm
from jobs.permission import *

User = get_user_model()

# Create your views here.


@login_required(login_url=reverse_lazy("accounts:login"))
def create_resume_view(request):
    resume_form = ResumeForm(request.POST or None)
    user = get_object_or_404(User, id=request.user.id)

    if request.method == "POST" and resume_form.is_valid():
        instance = resume_form.save(commit=False)
        instance.user = user
        instance.save()
        messages.success(request, "You have created your resume.")
        return redirect(reverse("createresume:resume", kwargs={"id": instance.id}))

    context = {"resume_form": resume_form}
    return render(request, "resume/resume-form.html", context)


def resume_detail_view(request, id):
    resume = get_object_or_404(Resume, id=id)

    context = {
        "resume": resume,
    }
    return render(request, "resume/resume.html", context)


@login_required(login_url=reverse_lazy("accounts:login"))
def extract_pdf_text(request):
    if request.method == "POST":
        pdf_file = request.FILES.get("pdf_file")
        if pdf_file.content_type == "application/pdf":
            pdf = PdfReader(pdf_file)
            page = pdf.pages[0]
            text = page.extract_text()
            messages.success(request, "You have extracted text from pdf file.")
            context = {"text": text}
            return render(request, "resume/pdf_text.html", context)
        else:
            return redirect("upload_pdf")
    return render(request, "resume/upload_pdf.html")
