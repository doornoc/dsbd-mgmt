from django.apps import AppConfig


class CustomAuth(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mgmt.custom_auth'
    verbose_name = 'カスタムユーザ'

    def ready(self):
        from . import signals
