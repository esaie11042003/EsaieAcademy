from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "is_staff",
        "is_superuser",
        "actif",
    )
    list_filter = ("role", "is_staff", "is_superuser", "actif")

    fieldsets = UserAdmin.fieldsets + (
        ("Informations Esaïe Academy", {
            "fields": (
                "role",
                "niveau_etude",
                "sexe",
                "date_naissance",
                "adresse",
                "phone",
                "profile_picture",
                "is_verified",
                "must_change_password",
                "actif",
                "deleted",
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informations Esaïe Academy", {
            "fields": ("role",)
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
