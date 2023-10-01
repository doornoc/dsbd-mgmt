from django.core import validators
from django.db import models
from django.utils import timezone

from mgmt.custom_auth.models import User


class ServiceManager(models.Manager):
    print("")


class Server(models.Model):
    created_at = models.DateTimeField("作成日", default=timezone.now, db_index=True)
    is_active = models.BooleanField("有効", default=True)
    start_ip = models.GenericIPAddressField("Start IP", )
    size = models.IntegerField("Size", validators=[
        validators.MinValueValidator(0),
        validators.MaxValueValidator(32)
    ])
    gateway_ip = models.GenericIPAddressField("Gateway IP(Local)", )
    global_ip = models.GenericIPAddressField("Global IP", )
    global_port = models.IntegerField("Global Port", default=51820)
    mgmt_ip = models.GenericIPAddressField("Management IP", )
    mgmt_port = models.IntegerField("Management Port", default=8080)
    private_key = models.CharField("秘密鍵", max_length=250)
    public_key = models.CharField("公開鍵", max_length=250)
    comment = models.CharField("コメント", max_length=250, default='')

    class Meta:
        verbose_name = 'Wireguardサーバ'
        verbose_name_plural = "Wireguardサーバ"

    def __str__(self):
        return "%d: (GIP: %s) (MIP:%s)" % (self.id, self.global_ip, self.mgmt_ip)


def init_gen_count():
    count_array = []
    for client in Client.objects.all():
        count_array.append(client.count)
    count_array.sort()
    tmp_count = 1
    for value in count_array:
        if tmp_count == value:
            tmp_count = value + 1
        else:
            break
    return tmp_count


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField("作成日", default=timezone.now, db_index=True)
    is_active = models.BooleanField("有効", default=True)
    count = models.IntegerField("count", default=init_gen_count)
    public_key = models.CharField("公開鍵", max_length=250)
    comment = models.CharField("コメント", max_length=250, default='')

    objects = ServiceManager()

    class Meta:
        verbose_name = 'Wireguardサービス'
        verbose_name_plural = "Wireguardサービス"

    def __str__(self):
        return "%d: %s" % (self.id, self.count,)
