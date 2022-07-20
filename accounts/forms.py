from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create form here.
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder':'Enter Username', 'autoFocus': True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'eg: abc@jobsnp.com', 'required' : True}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Enter Same Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']