from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.core.serializers import serialize
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
            request, "You are successfully posted your job!"
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
        return redirect(reverse("jobs:job-detail", kwargs={"id": instance.id}))
    context = {"form": form, "categories": categories}

    return render(request, "jobs/update-job.html", context)


@login_required(login_url=reverse_lazy("accounts:login"))
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

    context = {
        "job": job,
    }
    return render(request, "jobs/jobs-list.html", context)


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_jobseeker
def apply_job_view(request, id):
    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, job=id)
    form = JobApplyForm(request.POST or None)
    if not applicant:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()
                messages.success(
                    request, 'You have successfully applied for this job!')
                return redirect(reverse("jobs:job-detail", kwargs={
                    'id': id
                }))
        else:
            return redirect(reverse("jobs:job-detail", kwargs={
                'id': id
            }))
    else:
        messages.error(request, 'You already applied for the Job!')
        return redirect(reverse("jobs:job-detail", kwargs={
            'id': id
        }))

@login_required(login_url=reverse_lazy("accounts:login"))
def dashboard_view(request):
    jobs = []
    appliedjobs = []
    total_applicants = {}
    if request.user.role == "employer":

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == "jobseeker":
        appliedjobs = Applicant.objects.filter(user=request.user.id)
    context = {
        "jobs": jobs,
        "appliedjobs": appliedjobs,
        "total_applicants": total_applicants,
    }

    return render(request, "jobs/dashboard.html", context)


@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_employer
def make_complete_job_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        try:
            job.is_closed = True
            job.save()
            messages.success(request, "Your Job was marked closed!")
        except:
            messages.success(request, "Something went wrong !")

    return redirect("jobs:dashboard")


@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_employer
def all_applicants_view(request, id):

    all_applicants = Applicant.objects.filter(job=id)

    context = {"all_applicants": all_applicants}

    return render(request, "jobs/all-applicants.html", context)


@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_employer
def applicant_details_view(request, id):

    applicant = get_object_or_404(User, id=id)

    context = {"applicant": applicant}

    return render(request, "jobs/applicant-details.html", context)

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_jobseeker
def job_bookmark_view(request, id):

    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully save this job!')
                return redirect(reverse("jobs:job-detail", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobs:job-detail", kwargs={
                'id': id
            }))

    else:
        messages.error(request, 'You already saved this Job!')

        return redirect(reverse("jobs:job-detail", kwargs={
            'id': id
        }))

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_jobseeker
def delete_bookmark_view(request, id):

    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Saved Job was successfully deleted!')

    return redirect('jobs:dashboard')