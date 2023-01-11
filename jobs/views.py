from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from accounts.models import User
from .models import *
from .forms import *
from .permission import *

User = get_user_model()

# Create your views here.
def home(request):
    return render(request, "index.html")


@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_employer
def post_job_view(request):
    job_form = JobForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == "POST" and job_form.is_valid():
        instance = job_form.save(commit=False)
        instance.user = user
        instance.save()
        # for save tags
        job_form.save_m2m()
        messages.success(
            request, "You are successfully posted your job! Please wait for review."
        )
        return redirect(reverse("jobs:job-detail", kwargs={"id": instance.id}))

    context = {"job_form": job_form, "categories": categories}
    return render(request, "jobs/post-job.html", context)


@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_employer
def update_job_view(request, id=id):
    job = get_object_or_404(Job, id=id, user=request.user.id)
    categories = Category.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, "Your Job Post Was Successfully Updated!")
        return redirect(reverse("jobs:detail-job", kwargs={"id": instance.id}))
    context = {"form": form, "categories": categories}

    return render(request, "jobs/update-job.html", context)


@login_required(login_url=reverse_lazy("account:login"))
@user_is_employer
def delete_job_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        job.delete()
        messages.success(request, "Your Job Post was deleted successfully!")

    return redirect("jobs:dashboard")


def job_detail_view(request, id):
    job = get_object_or_404(Job, id=id)

    context = {
        "job": job,
    }
    return render(request, "jobs/job-detail.html", context)


def jobs_list_view(request):
    job = Job.objects.all()
    return render(request, "jobs/jobs-list.html", {"job": job})
