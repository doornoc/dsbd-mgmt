from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from mgmt.wireguard.api import wg_delete_all, wg_delete, wg_overwrite_all, wg_create, wg_update, wg_overwrite
from mgmt.wireguard.models import Client, Server


@receiver(pre_save, sender=Server)
def create_server(sender, instance, **kwargs):
    if instance.is_active:
        wg_overwrite(instance)

@receiver(pre_save, sender=Server)
def update_server(sender, instance, **kwargs):
    if instance.id is not None:
        prev = Server.objects.get(id=instance.id)
        if prev.is_active != instance.is_active:
            if instance.is_active:
                wg_overwrite(instance)
            else:
                wg_delete_all(instance)


@receiver(pre_delete, sender=Client)
def delete_server(sender, instance, **kwargs):
    wg_delete_all(instance)


@receiver(pre_save, sender=Client)
def create_client(sender, instance, **kwargs):
    try:
        if instance.id is None and instance.is_active:
            wg_create(instance)
    except:
        print("ERROR")


@receiver(pre_save, sender=Client)
def update_client(sender, instance, **kwargs):
    try:
        if instance.id is not None:
            prev = Client.objects.get(id=instance.id)
            if prev.is_active != instance.is_active:
                if instance.is_active:
                    wg_create(instance)
                else:
                    wg_delete(instance.public_key)
            elif prev.public_key != instance.public_key:
                wg_update(prev.public_key, instance)
    except:
        print("ERROR")


@receiver(pre_delete, sender=Client)
def delete_client(sender, instance, created, **kwargs):
    wg_delete(instance.public_key)
