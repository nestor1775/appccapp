from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Importa las señales para que se registren
        import api.signals  # Asegúrate de que las señales se registren
