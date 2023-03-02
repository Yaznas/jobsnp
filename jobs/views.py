from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from PyPDF2 import PdfReader
import re

from accounts.models import User
from .models import *
from .forms import *
from .permission import *
from django.db.models import Q

User = get_user_model()

# Create your views here.
def home(request):
    published_jobs = Job.objects.filter(is_published=True).order_by("-timestamp")
    jobs = published_jobs.filter(is_closed=False)
    paginator = Paginator(jobs, 4)
    page_number = request.GET.get("page", None)
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "total_jobs": len(jobs)}

    return render(request, "index.html", context)


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
            request,
            "You have successfully posted your job! Also, An Email Notification has been sent to Jobseekers!",
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
    job = Job.objects.all().order_by("id")
    paginator = Paginator(job, 5)  # Show 5 jobs per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "jobs/jobs-list.html", context)


@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_jobseeker
def apply_job_view(request, id):
    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, job=id)
    form = JobApplyForm(request.POST or None)
    if not applicant:
        if request.method == "POST":
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()
                messages.success(request, "You have successfully applied for this job!")
                return redirect(reverse("jobs:job-detail", kwargs={"id": id}))
        else:
            return redirect(reverse("jobs:job-detail", kwargs={"id": id}))
    else:
        messages.error(request, "You already applied for the Job!")
        return redirect(reverse("jobs:job-detail", kwargs={"id": id}))


@login_required(login_url=reverse_lazy("accounts:login"))
def dashboard_view(request):
    jobs = []
    bookmarkedjobs = []
    appliedjobs = []
    total_applicants = {}
    if request.user.role == "employer":

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == "jobseeker":
        bookmarkedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)

    context = {
        "jobs": jobs,
        "bookmarkedjobs": bookmarkedjobs,
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
            messages.success(request, "Something went wrong!")

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


@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_jobseeker
def job_bookmark_view(request, id):

    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

    if not applicant:
        if request.method == "POST":

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(request, "You have successfully bookmarked this job!")
                return redirect(reverse("jobs:job-detail", kwargs={"id": id}))

        else:
            return redirect(reverse("jobs:job-detail", kwargs={"id": id}))

    else:
        messages.error(request, "You already bookmarked this Job!")

        return redirect(reverse("jobs:job-detail", kwargs={"id": id}))


@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_jobseeker
def delete_bookmark_view(request, id):

    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, "Bookmarked Job was successfully deleted!")

    return redirect("jobs:dashboard")


def search_job_view(request):
    job_list = Job.objects.all().order_by("-timestamp")

    if "job_title_or_company_name" in request.GET:
        job_title_or_company_name = request.GET["job_title_or_company_name"]

        if job_title_or_company_name:
            job_list = job_list.filter(
                title__icontains=job_title_or_company_name
            ) | job_list.filter(company_name__icontains=job_title_or_company_name)

    if "location" in request.GET:
        location = request.GET["location"]

        if location:
            job_list = job_list.filter(location__icontains=location)

    if "job_type" in request.GET:
        job_type = request.GET["job_type"]
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    paginator = Paginator(job_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "jobs/search-job.html", context)


@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_employer
def send_feedback(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    if request.method == "POST":
        form = FeedbackMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            messages.success(request, "You have successfully sent your feedback.")
            return redirect(
                reverse("jobs:applicant-details", kwargs={"id": receiver_id})
            )
    else:
        form = FeedbackMessageForm()
        context = {"form": form}
    return render(request, "send_feedback.html", context)


@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_jobseeker
def see_feedback(request):
    user_messages = FeedbackMessage.objects.filter(receiver=request.user)
    context = {"user_messages": user_messages}
    return render(request, "user-feedback.html", context)

@login_required(login_url=reverse_lazy("accounts:login"))
def extract_pdf_text(request):
    if request.method == "POST":
        # Extract text from uploaded pdf file.
        pdf_file = request.FILES.get("pdf_file")
        try:
            pdf = PdfReader(pdf_file)
            extracted_text = ''
            for page in pdf.pages:
                extracted_text += page.extract_text()
            
            cleaned_text = re.sub('\x00', '', extracted_text)
            cleaned_text = cleaned_text.split()

            # Search for text in job models.
            q_filters = Q()
            for text in cleaned_text:
                q_filters |= Q(title__icontains=text)
            
            matching_jobs = Job.objects.filter(q_filters)

            context = {"extracted_text": cleaned_text, "matching_jobs": matching_jobs}
            messages.success(request, "Text extracted and jobs matching your resume have been found.")
            return render(request, "resume/pdf_text.html", context)
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, "resume/upload_pdf.html")
    return render(request, "resume/upload_pdf.html")
