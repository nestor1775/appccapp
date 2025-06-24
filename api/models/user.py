from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROL_CHOICES = [
        ('admin', 'Administrator'),
        ('worker', 'Worker'),
    ]
    role = models.CharField(max_length=20, choices=ROL_CHOICES)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})" 