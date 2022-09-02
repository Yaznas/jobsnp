from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Job
from .forms import JobForm

# Create your views here.
def home(request):
    return render(request, 'index.html')

def post_job_view(request):
    job_form = JobForm()
    if request.method == 'POST':
        job_form = JobForm(request.POST)
        if job_form.is_valid():
            job_form.save()
            return redirect('job-list')
        else:
            return HttpResponse("Your Entered Information is incorrect")
    else:
        return render(request, 'jobs/post-job.html', {'job_form':job_form})

def job_list_view(request):
    job = Job.objects.all()
    return render(request, 'jobs/job-list.html', {'job':job})

def job_update_view(request, job_id):
    job_id = int(job_id)
    try:
        job_sel = Job.objects.get(id = job_id)
    except Job.DoesNotExist:
        return redirect('home')
    jobupdate_form = JobForm(request.POST or None, instance = job_sel)
    if jobupdate_form.is_valid():
        jobupdate_form.save()
        return redirect('home')
    return render(request, 'jobs/post-job.html', {'job_form':jobupdate_form})

def job_delete_view(request, job_id):
        job_id = int(job_id)
        try:
            job_sel = Job.objects.get(id = job_id)
        except Job.DoesNotExist:
            return redirect('index')
        job_sel.delete()
        return redirect('home')
