from django.contrib import admin
from .models import Evaluation, Note


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):

    list_display = (
        "assignment",
        "period",
        "evaluation_type",
        "numero",
        "date",
        "note_sur",
        "statut",
        "publier",
    )

    list_filter = (
        "period",
        "evaluation_type",
        "statut",
        "publier",
    )

    search_fields = (
        "assignment__teacher__user__first_name",
        "assignment__teacher__user__last_name",
        "assignment__teacher__user__username",
        "assignment__subject__nom",
        "assignment__classe__nom",
    )

    ordering = (
        "period",
        "assignment",
        "evaluation_type",
        "numero",
    )

    list_editable = (
        "statut",
        "publier",
    )

    date_hierarchy = "date"

    list_per_page = 20


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):

    list_display = (
        "eleve",
        "evaluation",
        "note",
        "absent",
        "created_at",
    )

    list_filter = (
        "evaluation",
        "absent",
    )

    search_fields = (
        "eleve__nom",
        "eleve__prenom",
    )

    ordering = (
        "evaluation",
        "eleve",
    )

    list_editable = (
        "absent",
    )

    list_per_page = 30