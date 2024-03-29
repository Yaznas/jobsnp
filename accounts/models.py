from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

Gender = (
    ("M", "Male"),
    ("F", "Female"),
)

ROLE = (
    ("employer", "Employer"),
    ("jobseeker", "Jobseeker"),
)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    role = models.CharField(choices=ROLE, max_length=10)
    gender = models.CharField(choices=Gender, max_length=1, default=1)
    cv = models.FileField(upload_to="docs/", null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    objects = CustomUserManager()
