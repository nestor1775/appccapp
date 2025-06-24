from django.db import models
from .vessel import Vessel

class PredefinedMessage(models.Model):
    TYPE_CHOICES = [
        ('food', 'Food'),
        ('cleaning', 'Cleaning'),
        ('assistance', 'Assistance'),
    ]
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    content = models.TextField()

    def __str__(self):
        return f"{self.type} - {self.vessel.name}" 