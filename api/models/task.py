from django.db import models
from django.utils import timezone
from .message import PredefinedMessage
from .guest import Guest
from .room import Room
from .user import User
from .vessel import Vessel

class Task(models.Model):
    predefined_message = models.ForeignKey(PredefinedMessage, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, null=True, blank=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_tasks")
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_tasks")
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)

    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed")
    ], default="pending")

    creation_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.predefined_message.content} -> {self.assigned}" 