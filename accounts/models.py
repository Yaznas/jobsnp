from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User(AbstractUser):
    is_jobseeker = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class Jobseeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user.is_jobseeker = True
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=50)

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user.is_employer = True
    company_name = models.CharField(max_length=100)
    company_location = models.CharField(max_length=50)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_jobseeker:
            Jobseeker.objects.create(user=instance)
        elif instance.is_employer:
            Employer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_jobseeker:
        instance.jobseeker.save()
    elif instance.is_employer:
        instance.employer.save()