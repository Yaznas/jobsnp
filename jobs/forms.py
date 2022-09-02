from dataclasses import fields
from socket import fromshare
from django import forms
from .models import Job
from ckeditor.widgets import CKEditorWidget

class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['title', 'description', 'salary', 'location', 'job_type', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'class':'input', 'placeholder': 'Enter Job Title'}),
            'description': CKEditorWidget(),
            'salary': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Enter Estimated Salary'}),
            'location': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter Job Location'}),
            'url': forms.URLInput(attrs={'class': 'input', 'placeholder': 'Enter Website URL'}),
        }
        labels = {
            'job_type': 'Job Type',
            'url': 'Website',
        }

