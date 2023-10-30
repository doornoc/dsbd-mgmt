from django.contrib import admin

from .models import Device, Template, Auth


@admin.register(Device)
class Device(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("created_at", "is_active", "comment")}),
        ('Global', {'fields': ('hostname', 'address', 'template', 'auth')}),
    )
    list_display = ("id", "is_active", "hostname", "address",)
    list_filter = ("is_active",)
    search_fields = ("is_active",)


@admin.register(Template)
class Template(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("created_at", "is_active", "category1", "category2", "category3", "comment")}),
        ('info', {'fields': ('commands', 'ignore_lines', 'config_start', 'config_end')}),
    )
    list_display = ("id", "category1", "category2", "category3")
    list_filter = ("is_active",)
    search_fields = ("is_active",)


@admin.register(Auth)
class Auth(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("created_at", "is_active", "comment")}),
        ('info', {'fields': ('access_type', 'username', 'password', "public_key")}),
    )
    list_display = ("id", "access_type", "username",)
    list_filter = ("is_active",)
    search_fields = ("is_active",)
