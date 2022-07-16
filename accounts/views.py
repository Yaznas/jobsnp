from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}, Your account is created.')
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render (request, 'users/register.html', context)