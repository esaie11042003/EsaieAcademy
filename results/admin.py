from django.contrib import admin
from .models import StudentResult


@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):

    list_display = (
        "eleve",
        "period",
        "moyenne_generale",
        "total_points",
        "total_coefficients",
        "rang",
        "mention",
        "decision",
    )

    list_filter = (
        "period",
        "decision",
    )

    search_fields = (
        "eleve__nom",
        "eleve__prenom",
    )

    ordering = (
        "period",
        "rang",
    )

    list_per_page = 25