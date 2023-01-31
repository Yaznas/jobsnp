from django import forms
from .models import Resume
from ckeditor.widgets import CKEditorWidget


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = (
            "name",
            "email",
            "phone",
            "location",
            "about",
            "education",
            "projects",
            "work",
            "skills",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Your Full Name"}
            ),
            "email": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your Email"}
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number",
                }
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Your Location"}
            ),
            "about": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter your information"}
            ),
            "education": CKEditorWidget(),
            "projects": CKEditorWidget(),
            "work": CKEditorWidget(),
            "skills": CKEditorWidget(),
        }

    def save(self, commit=True):
        job = super(ResumeForm, self).save(commit=False)
        if commit:
            job.save()
        return job
