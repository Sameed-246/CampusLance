from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "role",
                "phone",
                "profile_image",
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "classes": ("wide",),
            "fields": (
                "role",
                "phone",
                "profile_image",
            ),
        }),
    )