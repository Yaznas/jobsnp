from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Job(models.Model):
    JOB_TYPE = (
        ('1', 'Full Time'),
        ('2', 'Part Time'),
        ('3', 'Internship'),
    )

    title = models.CharField(max_length=150)
    description = RichTextField()
    salary = models.DecimalField(max_digits=5, decimal_places=2)
    location = models.CharField(max_length=30)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1, default=1)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.title