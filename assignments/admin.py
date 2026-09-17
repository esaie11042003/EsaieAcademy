from django.contrib import admin
from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "teacher",
        "classe",
        "subject",
        "school_year",
        "coefficient",
        "active",
    )

    list_filter = (
        "school_year",
        "classe",
        "subject",
        "active",
    )

    search_fields = (
        "teacher__user__first_name",
        "teacher__user__last_name",
        "teacher__user__username",
        "classe__nom",
        "subject__name",
    )

    list_editable = (
        "coefficient",
        "active",
    )