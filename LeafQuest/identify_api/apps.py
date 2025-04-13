from django.apps import AppConfig


class IdentifyApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'identify_api'

    def ready(self):
        from . import signals
