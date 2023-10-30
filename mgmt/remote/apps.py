from django.apps import AppConfig


class Config(AppConfig):
    name = "mgmt.remote"
    verbose_name = "Remote"

    def ready(self):
        from . import signals