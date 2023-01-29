from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib import auth

from .models import *
from ckeditor.widgets import CKEditorWidget


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "description",
            "tags",
            "category",
            "salary",
            "location",
            "job_type",
            "company_name",
            "url",
            "last_date",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Job Title"}
            ),
            "description": CKEditorWidget(),
            "tags": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "tag1, tag2"}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "salary": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter Estimated Salary"}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Job Location"}
            ),
            "job_type": forms.Select(attrs={"class": "form-select"}),
            "company_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Company Name"}
            ),
            "url": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "Enter Website URL"}
            ),
            "last_date": forms.DateInput(attrs={"class": "form-control"}),
        }
        labels = {
            "job_type": "Job Type",
            "url": "Website",
        }

    def clean_job_type(self):
        job_type = self.cleaned_data.get("job_type")

        if not job_type:
            raise forms.ValidationError("It is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get("category")

        if not category:
            raise forms.ValidationError("Category is required")
        return category

    def save(self, commit=True):
        job = super(JobForm, self).save(commit=False)
        if commit:
            job.save()
        return job


class JobApplyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ["job"]


class JobBookmarkForm(forms.ModelForm):
    class Meta:
        model = BookmarkJob
        fields = ["job"]


class JobEditForm(forms.ModelForm):
    last_date = forms.CharField(widget=forms.DateInput(attrs={"class": "form-control"}))

    class Meta:
        model = Job
        fields = [
            "title",
            "description",
            "tags",
            "category",
            "salary",
            "location",
            "job_type",
            "company_name",
            "url",
            "last_date",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Job Title"}
            ),
            "description": CKEditorWidget(),
            "tags": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "tag1, tag2"}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "salary": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter Estimated Salary"}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Job Location"}
            ),
            "job_type": forms.Select(attrs={"class": "form-select"}),
            "company_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Company Name"}
            ),
            "url": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "Enter Website URL"}
            ),
        }
        labels = {
            "job_type": "Job Type",
            "url": "Website",
        }

    def clean_job_type(self):
        job_type = self.cleaned_data.get("job_type")

        if not job_type:
            raise forms.ValidationError("It is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get("category")

        if not category:
            raise forms.ValidationError("Category is required")
        return category

    def save(self, commit=True):
        job = super(JobEditForm, self).save(commit=False)
        if commit:
            job.save()
        return job
