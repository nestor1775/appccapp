from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from crewcall.notifications.services.firebase_service import enviar_notificacion

@receiver(post_save, sender=Task)
def notificar_nueva_tarea(sender, instance, created, **kwargs):
    """
    Envía una notificación cuando se crea una nueva tarea.
    """
    if created and instance.assigned:
        mensaje = f"Nueva tarea asignada: {instance.predefined_message.content}"
        enviar_notificacion(instance.assigned, mensaje)
