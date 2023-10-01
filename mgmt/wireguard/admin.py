from django.contrib import admin

from .models import Client, Server


@admin.register(Server)
class Server(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("created_at", "is_active", "comment")}),
        ('Global', {'fields': ('start_ip', 'size', 'gateway_ip', 'global_ip', 'global_port', 'mgmt_ip', 'mgmt_port')}),
        ('key', {'fields': ('private_key', 'public_key')}),
    )
    list_display = ("id", "created_at", "is_active", "private_key", "public_key",)
    list_filter = ("is_active",)
    search_fields = ("is_active",)


@admin.register(Client)
class Client(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("created_at", "is_active", "comment")}),
        ('info', {'fields': ('user', 'count', "public_key")}),
    )
    list_display = ("id", "count", "user",)
    list_filter = ("is_active",)
    search_fields = ("is_active",)
