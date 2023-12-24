from enum import Enum
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255)

    def __str__(self):
        if self.user:
            return f"{self.user.username}-{self.name}"
        else:
            return f"{self.name}-{self.phone}"


class JobTitle(Enum):
    GUARD = 'Guard'
    DIRECTOR = 'Director'
    DRIVER = 'Driver'


class Job(models.Model):
    JOB_CHOICES = [
        (JobTitle.GUARD.value, 'Guard'),
        (JobTitle.DIRECTOR.value, 'Director'),
        (JobTitle.DRIVER.value, 'Driver'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=20, choices=JOB_CHOICES, default=JobTitle.DRIVER.value)

    def __str__(self):
        return f"{self.user.username}-{self.job_title}"

