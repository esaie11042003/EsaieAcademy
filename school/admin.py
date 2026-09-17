from django.contrib import admin
from .models import SchoolYear, Period


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):

    list_display = (
        "nom",
        "date_debut",
        "date_fin",
        "active",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "nom",
    )

    ordering = (
        "-date_debut",
    )


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "school_year",
        "start_date",
        "end_date",
        "is_active",
    )

    list_filter = (
        "school_year",
        "is_active",
    )

    search_fields = (
        "school_year__nom",
    )

    ordering = (
        "school_year",
        "start_date",
    )