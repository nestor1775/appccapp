from django.db import models
from .vessel import Vessel
import uuid

class Guest(models.Model):
    name = models.CharField(max_length=100)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    guest_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f"{self.name} ({self.vessel.name})" 