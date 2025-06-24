from django.db import models
from .vessel import Vessel

class Room(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.vessel.name})" 