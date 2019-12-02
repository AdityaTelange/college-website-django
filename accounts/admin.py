from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from . import models


class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        # ("Personal info", {"fields": ("first_name", "last_name")},),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions",)},),
        ("Important dates", {"fields": ("last_login", "date_joined")},),)
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("username", "email", "password1", "password2"), },),)
    list_display = ("username", "email", "is_staff",)
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username", "email")


admin.site.register(models.User, UserAdmin)
