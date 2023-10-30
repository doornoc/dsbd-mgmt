from django.db import models
from django.utils import timezone

from mgmt.custom_auth.models import User
from mgmt.models import MediumTextField, LongTextField

ACCESS_TYPE_SSH = "ssh"
ACCESS_TYPE_TELNET = "telnet"

ACCESS_TYPE = (
    (ACCESS_TYPE_SSH, ACCESS_TYPE_SSH),
    (ACCESS_TYPE_TELNET, ACCESS_TYPE_TELNET),
)


class Template(models.Model):
    created_at = models.DateTimeField("作成日", default=timezone.now, db_index=True)
    name = models.CharField("名前", max_length=100)
    category1 = models.CharField("カテゴリ1", max_length=100)
    category2 = models.CharField("カテゴリ2", max_length=100, default='', blank=True, null=True)
    category3 = models.CharField("カテゴリ3", max_length=100, default='', blank=True, null=True)
    is_active = models.BooleanField("有効", default=True)
    commands = MediumTextField("commands", default='')
    ignore_lines = MediumTextField("ignore_lines", default='', blank=True, null=True)
    config_start = models.CharField("config_start", max_length=250, default='', blank=True, null=True)
    config_end = models.CharField("config_end", max_length=250, default='', blank=True, null=True)
    comment = models.CharField("コメント", max_length=250, default='', blank=True, null=True)

    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = "Template"

    def __str__(self):
        return "%d: %s/%s/%s" % (self.id, self.category1, self.category2, self.category3)


class Auth(models.Model):
    created_at = models.DateTimeField("作成日", default=timezone.now, db_index=True)
    is_active = models.BooleanField("有効", default=True)
    access_type = models.CharField("access_type", max_length=100, default="ssh", choices=ACCESS_TYPE)
    username = models.CharField("ユーザ名", max_length=250, default='')
    password = models.CharField("パスワード", max_length=250, default='', blank=True, null=True)
    ssh_key = models.CharField("SSH鍵", max_length=250, default='', blank=True, null=True)
    comment = models.CharField("コメント", max_length=250, default='', blank=True, null=True)

    class Meta:
        verbose_name = 'Auth'
        verbose_name_plural = "Auth"


class Device(models.Model):
    created_at = models.DateTimeField("作成日", default=timezone.now, db_index=True)
    updated_at = models.DateTimeField("更新日", default=timezone.now)
    is_active = models.BooleanField("有効", default=True)
    hostname = models.CharField("hostname", max_length=250, default='')
    address = models.GenericIPAddressField("Address", )
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    auth = models.ForeignKey(Auth, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.CharField("コメント", max_length=250, default='', blank=True, null=True)

    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = "Device"

    def __str__(self):
        return "%d: %s_%s" % (self.id, self.hostname, self.address)


class CollectorFailedLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    exec_time = models.DateTimeField("実行日", default=timezone.now, db_index=True)
    error = MediumTextField("error", default='', null=True, blank=True)

    class Meta:
        verbose_name = 'Collector Log'
        verbose_name_plural = "Collector Log"

    def __str__(self):
        return "%d (%s)" % (self.id, self.exec_time)


class RemoteLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, )
    exec_time = models.DateTimeField("実行日", default=timezone.now, db_index=True)
    success = models.BooleanField("成功", default=True)
    log = LongTextField("log", default='', null=True, blank=True)  # TODO: 入力時に名前と時間を記入

    class Meta:
        verbose_name = 'Remote Log'
        verbose_name_plural = "Remote Log"

    def __str__(self):
        return "%d (%d)" % (self.id, self.exec_time)
