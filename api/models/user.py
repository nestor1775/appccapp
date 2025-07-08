from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

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

class Device(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='devices')
    token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=20)  # 'android', 'ios', 'web'
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.platform}"