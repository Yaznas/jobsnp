from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login

from .models import User
from .forms import JobseekerSignUpForm, EmployerSignUpForm

# Create your views here.
def signup(request):
    return render(request, template_name='accounts/signup.html')

class JobseekerSignUpView(CreateView):
    model = User
    form_class = JobseekerSignUpForm
    template_name = 'accounts/jobseeker-signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class EmployerSignUpView(CreateView):
    model = User
    form_class = EmployerSignUpForm
    template_name = 'accounts/employer-signup.html'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')