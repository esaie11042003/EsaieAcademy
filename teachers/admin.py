from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "disponible",
        "date_inscription",
    )

    list_filter = (
        "disponible",
        "date_inscription",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    filter_horizontal = (
        "matieres",
        "classes",
    )