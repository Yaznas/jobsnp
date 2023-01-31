from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, null=True, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    user = models.ForeignKey(User, related_name="User", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name="Category", on_delete=models.CASCADE
    )
    JOB_TYPE = (
        ("1", "Full Time"),
        ("2", "Part Time"),
        ("3", "Internship"),
    )

    title = models.CharField(max_length=150)
    description = RichTextField()
    tags = TaggableManager()
    salary = models.CharField(max_length=30, blank=True, null=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1, default=1)
    company_name = models.CharField(max_length=300, null=True)
    url = models.URLField(max_length=200, null=True)
    last_date = models.DateField(null=True)
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applicants")
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.job.title


class BookmarkJob(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="bookmarks")
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.job.title


class FeedbackMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
