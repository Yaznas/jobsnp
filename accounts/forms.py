from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import *

# Create form here.
class JobseekerSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter First Name"}
        ),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Last Name"}
        ),
    )

    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields["password1"].label = "Password:"
        self.fields["password2"].label = "Confirm Password:"
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter Password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        )

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "gender",
        ]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter E-mail"}
            ),
            "gender": forms.RadioSelect(attrs={"class": "form-check-inline"}),
        }

    def clean_gender(self):
        gender = self.cleaned_data.get("gender")
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "jobseeker"
        if commit:
            user.save()
        return user


class EmployerSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter First Name"}
        ),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Last Name"}
        ),
    )

    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields["password1"].label = "Password:"
        self.fields["password2"].label = "Confirm Password:"
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter Password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "gender",
        ]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter E-mail"}
            ),
            "gender": forms.RadioSelect(attrs={"class": "form-check-inline"}),
        }

    def clean_gender(self):
        gender = self.cleaned_data.get("gender")
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
            }
        )
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
            }
        ),
    )

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("User Does Not Exist.")

            if not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")

            if not user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class JobseekerProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JobseekerProfileEditForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(
            {
                "placeholder": "Enter First Name",
            }
        )
        self.fields["last_name"].widget.attrs.update(
            {
                "placeholder": "Enter Last Name",
            }
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender"]
