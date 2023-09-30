from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mgmt.custom_auth.models import User, SignUpKey, UserActivateToken


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',)}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )
    list_display = ('username', 'email', 'is_staff',)
    list_filter = ("is_staff", "is_active",)
    search_fields = ('username', 'email')


@admin.register(SignUpKey)
class AdminSignUpKey(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("key", "comment", "expired_at", 'is_used')}),
        ('Important dates', {'fields': ('created_at',)}),
    )
    list_display = ('key', 'comment', 'expired_at', 'is_used')
    search_fields = ('key', 'expired_at', 'is_used')


@admin.register(UserActivateToken)
class AdminUserActivateToken(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("user", "token", "expired_at", "is_used")}),
        ('Important dates', {'fields': ('created_at',)}),
    )
    list_display = ('user', 'token', 'expired_at', 'is_used')
    search_fields = ('user', 'token', 'expired_at', 'is_used')
