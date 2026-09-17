from django.contrib import admin
from .models import Forum, ForumMessage


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ("nom", "actif", "cree_par", "created_at")
    list_filter = ("actif",)
    search_fields = ("nom", "description")
    filter_horizontal = ("participants",)


@admin.register(ForumMessage)
class ForumMessageAdmin(admin.ModelAdmin):
    list_display = ("forum", "auteur", "created_at")
    list_filter = ("forum",)