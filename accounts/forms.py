from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Jobseeker, Employer

# Create form here.
class JobseekerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'location', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        jobseeker = Jobseeker.objects.create(user=user)
        jobseeker.phone_number=self.cleaned_data.get('phone_number')
        jobseeker.location=self.cleaned_data.get('location')
        jobseeker.save()
        return user

class EmployerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    company_name = forms.CharField(required=True)
    company_location = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'company_name', 'company_location', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        employer = Employer.objects.create(user=user)
        employer.company_name = self.cleaned_data.get('company_name')
        employer.company_location = self.cleaned_data.get('company_location')
        employer.save()
        return user