from django.apps import AppConfig


class Wireguard(AppConfig):
    name = "mgmt.wireguard"
    verbose_name = "Wireguard"

    def ready(self):
        from . import signals