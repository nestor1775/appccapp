from django.db import models
from django.db.models import Q
from .user import User
import string
import random

class Vessel(models.Model):
    name = models.CharField(max_length=100)
    guest_pin = models.CharField(max_length=8, unique=True)
    logo_url = models.URLField(null=True, blank=True)
    unique_code = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = self._generate_unique_code()
        if not self.guest_pin:
            self.guest_pin = self._generate_unique_guest_pin()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        chars = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(random.choices(chars, k=8))
            if not Vessel.objects.filter(unique_code=code).exists():
                return code

    def _generate_unique_guest_pin(self):
        while True:
            pin = ''.join(random.choices(string.digits, k=6))
            if not Vessel.objects.filter(guest_pin=pin).exists():
                return pin

class UserVessel(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('worker', 'Worker'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('revoked', 'Revoked'),
        ('pending', 'Pending'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    role_in_vessel = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['user', 'vessel'], name='unique_user_per_vessel'),
        models.UniqueConstraint(
            fields=['vessel'],
            condition=Q(is_primary=True),
            name='only_one_primary_per_vessel'
        )
    ]

    def aprove(self):
        self.status= "active"
        self.save()

    def revoke(self):
        self.status= "revoked"
        self.save()

    
    def __str__(self):
        return f"{self.user.username} - {self.vessel.name} ({self.role_in_vessel})" 