from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Resume(models.Model):
    user = models.ForeignKey(User, related_name='resume_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    about = models.TextField(max_length=1000)
    education = RichTextField()
    projects = RichTextField()
    work = RichTextField()
    skills = RichTextField()

    def __str__(self):
        return self.name
