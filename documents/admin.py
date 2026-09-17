"""
==========================================================
                    ADMIN - DOCUMENTS
==========================================================

Application : Documents
Projet : Esaïe Academy

Administration complète de :

✔ Catégories de documents
✔ Types de documents
✔ Documents
✔ Fichiers des documents
✔ Tags
✔ Association document/tag
✔ Téléchargements
✔ Favoris
✔ Commentaires
✔ Accès aux documents
✔ Consultations
✔ Notes (ratings)
✔ Signets
✔ Partages
✔ Journal de sécurité
✔ Collections
✔ Versions
✔ Notifications
✔ Signalements
✔ Statistiques

Compatible Django 6.x

==========================================================
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import (
    DocumentCategory,
    DocumentType,
    Document,
    DocumentFile,
    DocumentTag,
    DocumentTagRelation,
    DocumentDownload,
    DocumentFavorite,
    DocumentComment,
    DocumentAccess,
    DocumentView,
    DocumentRating,
    DocumentBookmark,
    DocumentShare,
    DocumentSecurityLog,
    DocumentCollection,
    DocumentVersion,
    DocumentNotification,
    DocumentReport,
    DocumentStatistic,
)


def _badge(text, color):
    return format_html(
        '<span style="color:white;background:{};'
        'padding:4px 10px;border-radius:8px;">{}</span>',
        color,
        text,
    )


# ==========================================================
#              CATÉGORIES DES DOCUMENTS
# ==========================================================

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    """
    Administration des catégories de documents.
    """

    list_display = (
        "name",
        "code",
        "display_order",
        "active_badge",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )

    list_filter = (
        "active",
    )

    ordering = (
        "display_order",
        "name",
    )

    list_editable = (
        "display_order",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Informations générales", {
            "fields": (
                "name",
                "code",
                "description",
            )
        }),
        ("Apparence", {
            "fields": (
                "icon",
                "color",
                "display_order",
            )
        }),
        ("État", {
            "fields": (
                "active",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Statut")
    def active_badge(self, obj):
        return _badge("Active", "#28a745") if obj.active else _badge("Inactive", "#dc3545")


# ==========================================================
#                 TYPES DE DOCUMENTS
# ==========================================================

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    """
    Administration des types de fichiers.
    """

    list_display = (
        "name",
        "code",
        "file_type",
        "extension",
        "max_size_mb",
        "display_order",
        "active_badge",
    )

    search_fields = (
        "name",
        "code",
        "extension",
        "mime_type",
    )

    list_filter = (
        "file_type",
        "active",
    )

    ordering = (
        "display_order",
        "name",
    )

    list_editable = (
        "display_order",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Informations générales", {
            "fields": (
                "name",
                "code",
                "file_type",
                "extension",
                "mime_type",
            )
        }),
        ("Apparence", {
            "fields": (
                "icon",
                "color",
                "display_order",
            )
        }),
        ("Limites", {
            "fields": (
                "max_size_mb",
            )
        }),
        ("État", {
            "fields": (
                "active",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Statut")
    def active_badge(self, obj):
        return _badge("Active", "#28a745") if obj.active else _badge("Inactive", "#dc3545")


# ==========================================================
#                    DOCUMENTS
# ==========================================================

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Administration du modèle principal Document.
    """

    list_display = (
        "title",
        "category",
        "document_type",
        "subject",
        "classe",
        "level",
        "access_type",
        "published_badge",
        "featured_badge",
        "publication_date",
    )

    search_fields = (
        "title",
        "slug",
        "short_description",
        "description",
    )

    list_filter = (
        "category",
        "document_type",
        "level",
        "access_type",
        "published",
        "featured",
        "downloadable",
        "active",
    )

    ordering = (
        "-publication_date",
        "title",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Informations générales", {
            "fields": (
                "title",
                "slug",
                "short_description",
                "description",
                "cover_image",
            )
        }),
        ("Classification", {
            "fields": (
                "category",
                "document_type",
                "subject",
                "classe",
                "school_year",
                "teacher",
                "level",
            )
        }),
        ("Accès", {
            "fields": (
                "access_type",
                "downloadable",
                "published",
                "publication_date",
                "featured",
            )
        }),
        ("Séries", {
            "fields": (
                "series",
            )
        }),
        ("État", {
            "fields": (
                "active",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    filter_horizontal = (
        "series",
    )

    @admin.display(description="Publié")
    def published_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.published else _badge("Non", "#dc3545")

    @admin.display(description="À la une")
    def featured_badge(self, obj):
        return _badge("Oui", "#ffc107") if obj.featured else _badge("Non", "#6c757d")


# ==========================================================
#                 FICHIERS DES DOCUMENTS
# ==========================================================

@admin.register(DocumentFile)
class DocumentFileAdmin(admin.ModelAdmin):
    """
    Administration des fichiers associés à un document.
    """

    list_display = (
        "title",
        "document",
        "file_type",
        "version",
        "file_size",
        "download_count",
        "main_file_badge",
    )

    search_fields = (
        "title",
        "document__title",
        "version",
    )

    list_filter = (
        "file_type",
        "is_main_file",
        "active",
    )

    ordering = (
        "document",
        "title",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "download_count",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Document concerné", {
            "fields": (
                "document",
                "file_type",
            )
        }),
        ("Fichier", {
            "fields": (
                "title",
                "file",
                "version",
                "file_size",
                "is_main_file",
            )
        }),
        ("Statistiques", {
            "fields": (
                "download_count",
            )
        }),
        ("État", {
            "fields": (
                "active",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Fichier principal")
    def main_file_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.is_main_file else _badge("Non", "#6c757d")


# ==========================================================
#                    TAGS DES DOCUMENTS
# ==========================================================

@admin.register(DocumentTag)
class DocumentTagAdmin(admin.ModelAdmin):
    """
    Administration des mots-clés (tags).
    """

    list_display = (
        "name",
        "slug",
        "color",
        "active_badge",
    )

    search_fields = (
        "name",
        "slug",
        "description",
    )

    list_filter = (
        "active",
    )

    ordering = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Informations générales", {
            "fields": (
                "name",
                "slug",
                "color",
                "description",
            )
        }),
        ("État", {
            "fields": (
                "active",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Statut")
    def active_badge(self, obj):
        return _badge("Active", "#28a745") if obj.active else _badge("Inactive", "#dc3545")


# ==========================================================
#              ASSOCIATION DOCUMENT <-> TAG
# ==========================================================

@admin.register(DocumentTagRelation)
class DocumentTagRelationAdmin(admin.ModelAdmin):
    """
    Administration des associations document/tag.
    """

    list_display = (
        "document",
        "tag",
        "active_badge",
    )

    search_fields = (
        "document__title",
        "tag__name",
    )

    list_filter = (
        "active",
        "tag",
    )

    ordering = (
        "document",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Association", {
            "fields": (
                "document",
                "tag",
            )
        }),
        ("État", {
            "fields": (
                "active",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Statut")
    def active_badge(self, obj):
        return _badge("Active", "#28a745") if obj.active else _badge("Inactive", "#dc3545")


# ==========================================================
#          HISTORIQUE DES TÉLÉCHARGEMENTS
# ==========================================================

@admin.register(DocumentDownload)
class DocumentDownloadAdmin(admin.ModelAdmin):
    """
    Historique des téléchargements de documents.
    """

    list_display = (
        "document",
        "user",
        "file",
        "status_badge",
        "payment_verified_badge",
        "download_date",
    )

    search_fields = (
        "document__title",
        "user__username",
        "ip_address",
        "device",
    )

    list_filter = (
        "status",
        "payment_verified",
        "download_date",
    )

    ordering = (
        "-download_date",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "download_date",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Téléchargement", {
            "fields": (
                "document",
                "user",
                "file",
                "status",
                "payment_verified",
            )
        }),
        ("Informations techniques", {
            "classes": ("collapse",),
            "fields": (
                "ip_address",
                "device",
                "browser",
                "operating_system",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "download_date",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Statut")
    def status_badge(self, obj):
        colors = {
            "authorized": "#28a745",
            "blocked": "#dc3545",
            "expired": "#ffc107",
        }
        return _badge(obj.get_status_display(), colors.get(obj.status, "#6c757d"))

    @admin.display(description="Paiement vérifié")
    def payment_verified_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.payment_verified else _badge("Non", "#dc3545")


# ==========================================================
#                DOCUMENTS FAVORIS
# ==========================================================

@admin.register(DocumentFavorite)
class DocumentFavoriteAdmin(admin.ModelAdmin):
    """
    Administration des documents favoris.
    """

    list_display = (
        "user",
        "document",
        "favorite_date",
    )

    search_fields = (
        "user__username",
        "document__title",
        "note",
    )

    list_filter = (
        "favorite_date",
    )

    ordering = (
        "-favorite_date",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "favorite_date",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Favori", {
            "fields": (
                "user",
                "document",
                "note",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "favorite_date",
                "created_at",
                "updated_at",
            )
        }),
    )


# ==========================================================
#              COMMENTAIRES DES DOCUMENTS
# ==========================================================

@admin.register(DocumentComment)
class DocumentCommentAdmin(admin.ModelAdmin):
    """
    Administration des commentaires.
    """

    list_display = (
        "user",
        "document",
        "rating",
        "likes",
        "dislikes",
        "approved_badge",
        "reported_badge",
        "created_at",
    )

    search_fields = (
        "user__username",
        "document__title",
        "comment",
    )

    list_filter = (
        "is_approved",
        "is_pinned",
        "is_reported",
        "rating",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Commentaire", {
            "fields": (
                "document",
                "user",
                "parent",
                "comment",
                "rating",
            )
        }),
        ("Interactions", {
            "fields": (
                "likes",
                "dislikes",
            )
        }),
        ("Modération", {
            "fields": (
                "is_approved",
                "is_pinned",
                "is_reported",
                "report_reason",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Approuvé")
    def approved_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.is_approved else _badge("Non", "#dc3545")

    @admin.display(description="Signalé")
    def reported_badge(self, obj):
        return _badge("Oui", "#dc3545") if obj.is_reported else _badge("Non", "#28a745")


# ==========================================================
#            ACCÈS AUX DOCUMENTS
# ==========================================================

@admin.register(DocumentAccess)
class DocumentAccessAdmin(admin.ModelAdmin):
    """
    Administration des autorisations d'accès.
    """

    list_display = (
        "user",
        "document",
        "status_badge",
        "unlimited_badge",
        "start_date",
        "end_date",
    )

    search_fields = (
        "user__username",
        "document__title",
    )

    list_filter = (
        "status",
        "unlimited",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Accès", {
            "fields": (
                "user",
                "document",
                "status",
            )
        }),
        ("Durée", {
            "fields": (
                "start_date",
                "end_date",
                "unlimited",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Statut")
    def status_badge(self, obj):
        colors = {
            "active": "#28a745",
            "expired": "#ffc107",
            "blocked": "#dc3545",
        }
        return _badge(obj.get_status_display(), colors.get(obj.status, "#6c757d"))

    @admin.display(description="Illimité")
    def unlimited_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.unlimited else _badge("Non", "#6c757d")


# ==========================================================
#              HISTORIQUE DES CONSULTATIONS
# ==========================================================

@admin.register(DocumentView)
class DocumentViewAdmin(admin.ModelAdmin):
    """
    Historique des consultations des documents.
    """

    list_display = (
        "document",
        "user",
        "viewed_at",
        "ip_address",
    )

    search_fields = (
        "document__title",
        "user__username",
        "ip_address",
    )

    list_filter = (
        "viewed_at",
    )

    ordering = (
        "-viewed_at",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "viewed_at",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Consultation", {
            "fields": (
                "document",
                "user",
            )
        }),
        ("Informations techniques", {
            "classes": ("collapse",),
            "fields": (
                "ip_address",
                "device",
                "browser",
                "operating_system",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "viewed_at",
                "created_at",
                "updated_at",
            )
        }),
    )


# ==========================================================
#              NOTES DES DOCUMENTS
# ==========================================================

@admin.register(DocumentRating)
class DocumentRatingAdmin(admin.ModelAdmin):
    """
    Administration des notes attribuées aux documents.
    """

    list_display = (
        "document",
        "user",
        "rating",
        "created_at",
    )

    search_fields = (
        "document__title",
        "user__username",
        "review",
    )

    list_filter = (
        "rating",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Note", {
            "fields": (
                "document",
                "user",
                "rating",
                "review",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )


# ==========================================================
#               SIGNETS DES DOCUMENTS
# ==========================================================

@admin.register(DocumentBookmark)
class DocumentBookmarkAdmin(admin.ModelAdmin):
    """
    Administration des signets (reprise de lecture).
    """

    list_display = (
        "user",
        "document",
        "page_number",
        "video_position",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "document__title",
        "note",
    )

    list_filter = (
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Signet", {
            "fields": (
                "user",
                "document",
                "page_number",
                "video_position",
                "note",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )


# ==========================================================
#             PARTAGE DES DOCUMENTS
# ==========================================================

@admin.register(DocumentShare)
class DocumentShareAdmin(admin.ModelAdmin):
    """
    Administration du partage des documents.
    """

    list_display = (
        "document",
        "shared_by",
        "shared_with",
        "share_type",
        "download_allowed_badge",
        "active_badge",
    )

    search_fields = (
        "document__title",
        "shared_by__username",
        "shared_with__username",
    )

    list_filter = (
        "share_type",
        "download_allowed",
        "active",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Partage", {
            "fields": (
                "document",
                "shared_by",
                "shared_with",
                "share_type",
            )
        }),
        ("Durée", {
            "fields": (
                "access_start",
                "access_end",
            )
        }),
        ("Options", {
            "fields": (
                "download_allowed",
                "active",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Téléchargement autorisé")
    def download_allowed_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.download_allowed else _badge("Non", "#dc3545")

    @admin.display(description="Actif")
    def active_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.active else _badge("Non", "#dc3545")


# ==========================================================
#            JOURNAL DE SÉCURITÉ DES DOCUMENTS
# ==========================================================

@admin.register(DocumentSecurityLog)
class DocumentSecurityLogAdmin(admin.ModelAdmin):
    """
    Journal des actions de sécurité sur les documents.
    """

    list_display = (
        "action",
        "document",
        "user",
        "success_badge",
        "created_at",
    )

    search_fields = (
        "document__title",
        "user__username",
        "message",
        "ip_address",
    )

    list_filter = (
        "action",
        "success",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Action", {
            "fields": (
                "document",
                "user",
                "action",
                "success",
            )
        }),
        ("Informations techniques", {
            "classes": ("collapse",),
            "fields": (
                "ip_address",
                "device",
                "browser",
                "operating_system",
            )
        }),
        ("Détails", {
            "fields": (
                "message",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Réussi")
    def success_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.success else _badge("Non", "#dc3545")


# ==========================================================
#              COLLECTIONS DE DOCUMENTS
# ==========================================================

@admin.register(DocumentCollection)
class DocumentCollectionAdmin(admin.ModelAdmin):
    """
    Administration des collections de documents.
    """

    list_display = (
        "title",
        "public_badge",
        "featured_badge",
        "active_badge",
    )

    search_fields = (
        "title",
        "slug",
        "description",
    )

    list_filter = (
        "is_public",
        "featured",
        "active",
    )

    ordering = (
        "title",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    filter_horizontal = (
        "documents",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Informations générales", {
            "fields": (
                "title",
                "slug",
                "description",
                "image",
            )
        }),
        ("Documents", {
            "fields": (
                "documents",
            )
        }),
        ("Options", {
            "fields": (
                "is_public",
                "featured",
                "active",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Publique")
    def public_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.is_public else _badge("Non", "#dc3545")

    @admin.display(description="À la une")
    def featured_badge(self, obj):
        return _badge("Oui", "#ffc107") if obj.featured else _badge("Non", "#6c757d")

    @admin.display(description="Statut")
    def active_badge(self, obj):
        return _badge("Active", "#28a745") if obj.active else _badge("Inactive", "#dc3545")


# ==========================================================
#              HISTORIQUE DES VERSIONS
# ==========================================================

@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    """
    Administration de l'historique des versions.
    """

    list_display = (
        "document",
        "version",
        "title",
        "created_by",
        "current_badge",
        "created_at",
    )

    search_fields = (
        "document__title",
        "version",
        "title",
    )

    list_filter = (
        "is_current",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Version", {
            "fields": (
                "document",
                "version",
                "title",
                "file",
                "created_by",
                "is_current",
            )
        }),
        ("Description", {
            "fields": (
                "description",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Version actuelle")
    def current_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.is_current else _badge("Non", "#6c757d")


# ==========================================================
#           NOTIFICATIONS DES DOCUMENTS
# ==========================================================

@admin.register(DocumentNotification)
class DocumentNotificationAdmin(admin.ModelAdmin):
    """
    Administration des notifications liées aux documents.
    """

    list_display = (
        "recipient",
        "document",
        "notification_type",
        "title",
        "read_badge",
        "sent_at",
    )

    search_fields = (
        "recipient__username",
        "document__title",
        "title",
        "message",
    )

    list_filter = (
        "notification_type",
        "is_read",
    )

    ordering = (
        "-sent_at",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "sent_at",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Notification", {
            "fields": (
                "document",
                "recipient",
                "notification_type",
                "title",
                "message",
                "is_read",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "sent_at",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Lu")
    def read_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.is_read else _badge("Non", "#dc3545")


# ==========================================================
#            SIGNALEMENT DES DOCUMENTS
# ==========================================================

@admin.register(DocumentReport)
class DocumentReportAdmin(admin.ModelAdmin):
    """
    Administration des signalements de documents.
    """

    list_display = (
        "document",
        "reported_by",
        "report_type",
        "status_badge",
        "reviewed_by",
        "created_at",
    )

    search_fields = (
        "document__title",
        "reported_by__username",
        "description",
    )

    list_filter = (
        "report_type",
        "status",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Signalement", {
            "fields": (
                "document",
                "reported_by",
                "report_type",
                "description",
            )
        }),
        ("Traitement", {
            "fields": (
                "status",
                "reviewed_by",
                "reviewed_at",
                "admin_note",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Statut")
    def status_badge(self, obj):
        colors = {
            "pending": "#ffc107",
            "reviewing": "#17a2b8",
            "resolved": "#28a745",
            "rejected": "#dc3545",
        }
        return _badge(obj.get_status_display(), colors.get(obj.status, "#6c757d"))


# ==========================================================
#            STATISTIQUES DES DOCUMENTS
# ==========================================================

@admin.register(DocumentStatistic)
class DocumentStatisticAdmin(admin.ModelAdmin):
    """
    Administration des statistiques par document.
    """

    list_display = (
        "document",
        "total_views",
        "total_downloads",
        "total_favorites",
        "total_comments",
        "average_rating",
        "total_shares",
        "total_reports",
    )

    search_fields = (
        "document__title",
    )

    ordering = (
        "-total_views",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Document concerné", {
            "fields": (
                "document",
            )
        }),
        ("Statistiques principales", {
            "fields": (
                "total_views",
                "total_downloads",
                "total_favorites",
                "total_comments",
                "total_ratings",
                "average_rating",
                "total_shares",
                "total_reports",
            )
        }),
        ("Dernières activités", {
            "fields": (
                "last_view",
                "last_download",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "created_at",
                "updated_at",
            )
        }),
    )