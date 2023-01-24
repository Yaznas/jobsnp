from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from .forms import *
from jobs.permission import user_is_jobseeker

# Create your views here.
def signup(request):
    return render(request, template_name="accounts/signup.html")


def jobseeker_signup(request):
    form = JobseekerSignUpForm(request.POST, request.FILES)
    if form.is_valid():
        form = form.save()
        messages.success(request, "Your Account has been created. Login now!")
        return redirect("accounts:login")
    context = {"form": form}

    return render(request, "accounts/jobseeker-signup.html", context)


def employer_signup(request):
    form = EmployerSignUpForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        messages.success(request, "Your Account has been created. Login now!")
        return redirect("accounts:login")
    context = {"form": form}

    return render(request, "accounts/employer-signup.html", context)


def user_logIn(request):
    form = UserLoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect("/")

    else:
        if request.method == "POST":
            if form.is_valid():
                auth.login(request, form.get_user())
                return HttpResponseRedirect(get_success_url(request))
    context = {
        "form": form,
    }

    return render(request, "accounts/login.html", context)


def get_success_url(request):
    if "next" in request.GET and request.GET["next"] != "":
        return request.GET["next"]
    else:
        return reverse("jobs:home")


@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_jobseeker
def jobseeker_edit_profile(request, id=id):
    user = get_object_or_404(User, id=id)
    form = JobseekerProfileEditForm(request.POST or None, instance=user)
    if form.is_valid():
        form = form.save()
        messages.success(request, "Your Profile Was Successfully Updated!")
        return redirect(reverse("accounts:edit-profile", kwargs={"id": form.id}))
    context = {"form": form}

    return render(request, "accounts/jobseeker-edit-profile.html", context)

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')