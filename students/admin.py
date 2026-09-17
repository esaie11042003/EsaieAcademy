from django.contrib import admin
from .models import Eleve


@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "classe", "sexe")
    list_filter = ("classe", "sexe")
    search_fields = ("nom", "prenom")