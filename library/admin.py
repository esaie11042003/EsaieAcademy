"""
=============================================================
ESAIE ACADEMY

Application : Library

Administration Django

=============================================================
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import (
    LibraryCategory,
    LibraryAuthor,
    LibraryPublisher,
    LibraryCollection,
    LibraryBook,
    LibraryEdition,
    LibraryChapter,
    LibraryBookmark,
    LibraryReadingProgress,
    LibraryHistory,
    LibraryFavorite,
    LibraryRating,
    LibraryReview,
    LibraryBorrow,
    LibraryReservation,
    LibraryDownload,
    LibraryAnnotation,
    LibraryQuote,
    LibraryCertificate,
    LibraryRecommendation,
    LibraryStatistics,
)


# ==========================================================
# ACTIONS PERSONNALISEES
# ==========================================================

@admin.action(description="Publier les livres sélectionnés")
def publish_books(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description="Masquer les livres")
def unpublish_books(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.action(description="Archiver les livres")
def archive_books(modeladmin, request, queryset):
    queryset.update(archived=True)


@admin.action(description="Restaurer les livres")
def restore_books(modeladmin, request, queryset):
    queryset.update(archived=False)


@admin.action(description="Rendre gratuits")
def make_free(modeladmin, request, queryset):
    queryset.update(is_premium=False)


@admin.action(description="Rendre Premium")
def make_premium(modeladmin, request, queryset):
    queryset.update(is_premium=True)


# ==========================================================
# INLINES
# ==========================================================

class LibraryEditionInline(admin.TabularInline):
    model = LibraryEdition
    extra = 0
    show_change_link = True


class LibraryChapterInline(admin.TabularInline):
    model = LibraryChapter
    extra = 0
    show_change_link = True
    ordering = ("chapter_number", "order")


class LibraryDownloadInline(admin.TabularInline):
    model = LibraryDownload
    extra = 0
    readonly_fields = ("Eleve", "download_date")
    can_delete = False


class LibraryReviewInline(admin.TabularInline):
    model = LibraryReview
    extra = 0
    readonly_fields = ("Eleve", "created_at")


class LibraryRatingInline(admin.TabularInline):
    model = LibraryRating
    extra = 0
    readonly_fields = ("Eleve", "rating")


# ==========================================================
# LIVRES
# ==========================================================

@admin.register(LibraryBook)
class LibraryBookAdmin(admin.ModelAdmin):

    list_display = (
        "cover_preview",
        "title",
        "authors_display",
        "category",
        "subject",
        "language",
        "resource_type",
        "average_rating_display",
        "downloads_display",
        "views_display",
        "published_status",
        "premium_status",
        "active",
    )

    list_display_links = (
        "cover_preview",
        "title",
    )

    list_per_page = 30

    date_hierarchy = "created_at"

    ordering = (
        "-created_at",
    )

    search_fields = (
        "title",
        "subtitle",
        "isbn",
        "keywords",
        "summary",
        "authors__first_name",
        "authors__last_name",
        "publisher__name",
    )

    list_filter = (
        "category",
        "subject",
        "language",
        "resource_type",
        "is_published",
        "is_premium",
        "active",
        "archived",
        "created_at",
    )

    autocomplete_fields = (
        "authors",
        "publisher",
        "category",
    )

    filter_horizontal = (
        "authors",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "cover_preview_large",
        "total_downloads",
        "total_views",
        "total_reads",
        "average_rating",
        "total_favorites",
        "total_comments",
    )

    actions = (
        publish_books,
        unpublish_books,
        archive_books,
        restore_books,
        make_free,
        make_premium,
    )

    inlines = (
        LibraryEditionInline,
        LibraryChapterInline,
        LibraryDownloadInline,
        LibraryReviewInline,
        LibraryRatingInline,
    )

    fieldsets = (
        ("Informations générales", {
            "fields": (
                "title",
                "subtitle",
                "authors",
                "publisher",
                "collection",
                "category",
                "subject",
                "classe",
            )
        }),
        ("Description", {
            "fields": (
                "summary",
                "description",
                "keywords",
            )
        }),
        ("Publication", {
            "fields": (
                "publication_year",
                "edition_name",
                "isbn",
                "language",
            )
        }),
        ("Fichier", {
            "fields": (
                "document",
                "cover_preview_large",
            )
        }),
        ("Accès", {
            "fields": (
                "resource_type",
                "is_published",
                "is_premium",
                "is_public",
                "is_featured",
                "active",
                "archived",
            )
        }),
        ("Statistiques", {
            "classes": ("collapse",),
            "fields": (
                "total_views",
                "total_reads",
                "total_downloads",
                "total_favorites",
                "total_comments",
                "average_rating",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Couverture")
    def cover_preview(self, obj):
        cover = getattr(obj.document, "cover_image", None)
        if cover:
            return format_html('<img src="{}" width="45" height="60"/>', cover.url)
        return "-"

    @admin.display(description="Couverture")
    def cover_preview_large(self, obj):
        cover = getattr(obj.document, "cover_image", None)
        if cover:
            return format_html('<img src="{}" width="180"/>', cover.url)
        return "Aucune image"

    @admin.display(description="Auteurs")
    def authors_display(self, obj):
        return obj.author_names or "-"

    @admin.display(description="Publié", boolean=True)
    def published_status(self, obj):
        return obj.is_published

    @admin.display(description="Accès")
    def premium_status(self, obj):
        return "💎 Premium" if obj.is_premium else "Gratuit"

    @admin.display(description="Téléchargements")
    def downloads_display(self, obj):
        return obj.total_downloads

    @admin.display(description="Lectures")
    def views_display(self, obj):
        return obj.total_views

    @admin.display(description="Note")
    def average_rating_display(self, obj):
        return f"{obj.average_rating}/5"


# ==========================================================
# AUTEURS
# ==========================================================

@admin.register(LibraryAuthor)
class LibraryAuthorAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "nationality",
        "birth_date",
        "books_count",
        "active",
    )

    search_fields = (
        "first_name",
        "last_name",
        "biography",
    )

    list_filter = (
        "nationality",
        "active",
        "verified",
        "featured",
    )

    ordering = (
        "last_name",
        "first_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    @admin.display(description="Livres")
    def books_count(self, obj):
        return obj.books.count()


# ==========================================================
# EDITEURS
# ==========================================================

@admin.register(LibraryPublisher)
class LibraryPublisherAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "country",
        "website",
        "books_count",
        "active",
    )

    search_fields = (
        "name",
        "country",
    )

    list_filter = (
        "country",
        "active",
        "verified",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    @admin.display(description="Livres")
    def books_count(self, obj):
        return obj.books.count()


# ==========================================================
# CATEGORIES
# ==========================================================

@admin.register(LibraryCategory)
class LibraryCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "order",
        "books_count",
        "active",
    )

    search_fields = (
        "name",
        "description",
    )

    list_filter = (
        "active",
    )

    ordering = (
        "order",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    @admin.display(description="Livres")
    def books_count(self, obj):
        return obj.books.count()


# ==========================================================
# COLLECTIONS
# ==========================================================

@admin.register(LibraryCollection)
class LibraryCollectionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "school",
        "books_total",
        "public",
        "featured",
        "active",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
    )

    list_filter = (
        "public",
        "featured",
        "active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    @admin.display(description="Nombre de livres")
    def books_total(self, obj):
        return obj.books.count()


# ==========================================================
# EDITIONS
# ==========================================================

@admin.register(LibraryEdition)
class LibraryEditionAdmin(admin.ModelAdmin):

    list_display = (
        "book",
        "edition_name",
        "edition_number",
        "publication_year",
        "isbn",
        "is_latest",
    )

    search_fields = (
        "book__title",
        "isbn",
        "edition_name",
    )

    list_filter = (
        "is_latest",
        "available",
    )

    autocomplete_fields = (
        "book",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# ==========================================================
# CHAPITRES
# ==========================================================

@admin.register(LibraryChapter)
class LibraryChapterAdmin(admin.ModelAdmin):

    list_display = (
        "chapter_number",
        "title",
        "book",
        "page_start",
        "page_end",
        "is_published",
        "active",
    )

    search_fields = (
        "title",
        "book__title",
    )

    list_filter = (
        "active",
        "is_published",
        "is_free",
    )

    autocomplete_fields = (
        "book",
        "parent",
    )

    ordering = (
        "book",
        "chapter_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# ==========================================================
# SIGNETS
# ==========================================================

@admin.register(LibraryBookmark)
class LibraryBookmarkAdmin(admin.ModelAdmin):

    list_display = (
        "Eleve",
        "book",
        "page",
        "created_at",
    )

    search_fields = (
        "Eleve__nom",
        "Eleve__prenom",
        "book__title",
    )

    autocomplete_fields = (
        "Eleve",
        "book",
        "chapter",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )


# ==========================================================
# PROGRESSION
# ==========================================================

@admin.register(LibraryReadingProgress)
class LibraryReadingProgressAdmin(admin.ModelAdmin):

    list_display = (
        "Eleve",
        "book",
        "completion_percentage",
        "current_page",
        "minutes_read",
        "sessions",
        "completed",
    )

    search_fields = (
        "Eleve__nom",
        "Eleve__prenom",
        "book__title",
    )

    list_filter = (
        "completed",
    )

    autocomplete_fields = (
        "Eleve",
        "book",
        "current_chapter",
    )

    readonly_fields = (
        "minutes_read",
        "sessions",
        "last_read",
    )

    ordering = (
        "-updated_at",
    )


# ==========================================================
# HISTORIQUE
# ==========================================================

@admin.register(LibraryHistory)
class LibraryHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "Eleve",
        "book",
        "action",
        "page",
        "created_at",
    )

    search_fields = (
        "Eleve__nom",
        "Eleve__prenom",
        "book__title",
    )

    list_filter = (
        "action",
        "created_at",
    )

    autocomplete_fields = (
        "Eleve",
        "book",
        "chapter",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )


# ==========================================================
# TELECHARGEMENTS
# ==========================================================

@admin.register(LibraryDownload)
class LibraryDownloadAdmin(admin.ModelAdmin):

    list_display = (
        "Eleve",
        "book",
        "download_date",
        "device",
        "browser",
        "ip_address",
    )

    search_fields = (
        "Eleve__nom",
        "Eleve__prenom",
        "book__title",
    )

    list_filter = (
        "download_date",
    )

    autocomplete_fields = (
        "Eleve",
        "book",
        "chapter",
    )

    readonly_fields = (
        "download_date",
        "ip_address",
    )

    ordering = (
        "-download_date",
    )


# ==========================================================
# FAVORIS
# ==========================================================

@admin.register(LibraryFavorite)
class LibraryFavoriteAdmin(admin.ModelAdmin):

    list_display = (
        "Eleve",
        "book",
        "created_at",
    )

    search_fields = (
        "Eleve__nom",
        "Eleve__prenom",
        "book__title",
    )

    autocomplete_fields = (
        "Eleve",
        "book",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


# ==========================================================
# NOTES
# ==========================================================

@admin.register(LibraryRating)
class LibraryRatingAdmin(admin.ModelAdmin):

    list_display = (
        "Eleve",
        "book",
        "rating",
        "created_at",
    )

    search_fields = (
        "Eleve__nom",
        "Eleve__prenom",
        "book__title",
    )

    list_filter = (
        "rating",
    )

    autocomplete_fields = (
        "Eleve",
        "book",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


# ==========================================================
# AVIS
# ==========================================================

@admin.register(LibraryReview)
class LibraryReviewAdmin(admin.ModelAdmin):

    list_display = (
        "Eleve",
        "book",
        "title",
        "approved",
        "reported",
        "likes",
        "dislikes",
        "created_at",
    )

    search_fields = (
        "title",
        "review",
        "book__title",
    )

    list_filter = (
        "approved",
        "reported",
    )

    autocomplete_fields = (
        "Eleve",
        "book",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


# ==========================================================
# EMPRUNTS
# ==========================================================

@admin.register(LibraryBorrow)
class LibraryBorrowAdmin(admin.ModelAdmin):

    list_display = (
        "Eleve",
        "book",
        "borrow_date",
        "due_date",
        "return_date",
        "completed",
        "is_late",
    )

    search_fields = (
        "Eleve__nom",
        "Eleve__prenom",
        "book__title",
    )

    list_filter = (
        "completed",
        "renewed",
        "borrow_date",
        "due_date",
    )

    autocomplete_fields = (
        "Eleve",
        "book",
    )

    readonly_fields = (
        "borrow_date",
    )

    ordering = (
        "-borrow_date",
    )

    @admin.display(description="En retard", boolean=True)
    def is_late(self, obj):
        return obj.is_late


# ==========================================================
# RESERVATIONS
# ==========================================================

@admin.register(LibraryReservation)
class LibraryReservationAdmin(admin.ModelAdmin):

    list_display = (
        "Eleve",
        "book",
        "reservation_date",
        "expiration_date",
        "active",
        "notified",
    )

    search_fields = (
        "Eleve__nom",
        "Eleve__prenom",
        "book__title",
    )

    list_filter = (
        "active",
        "notified",
    )

    autocomplete_fields = (
        "Eleve",
        "book",
    )

    ordering = (
        "-reservation_date",
    )


# ==========================================================
# ANNOTATIONS
# ==========================================================

@admin.register(LibraryAnnotation)
class LibraryAnnotationAdmin(admin.ModelAdmin):

    list_display = (
        "Eleve",
        "book",
        "page",
        "created_at",
    )

    search_fields = (
        "selected_text",
        "note",
    )

    autocomplete_fields = (
        "Eleve",
        "book",
        "chapter",
    )

    readonly_fields = (
        "created_at",
    )


# ==========================================================
# CITATIONS
# ==========================================================

@admin.register(LibraryQuote)
class LibraryQuoteAdmin(admin.ModelAdmin):

    list_display = (
        "Eleve",
        "book",
        "page",
        "created_at",
    )

    search_fields = (
        "quote",
        "book__title",
    )

    autocomplete_fields = (
        "Eleve",
        "book",
    )

    readonly_fields = (
        "created_at",
    )


# ==========================================================
# CERTIFICATS
# ==========================================================

@admin.register(LibraryCertificate)
class LibraryCertificateAdmin(admin.ModelAdmin):

    list_display = (
        "certificate_number",
        "Eleve",
        "book",
        "score",
        "issue_date",
        "pdf_generated",
    )

    search_fields = (
        "certificate_number",
        "Eleve__nom",
        "Eleve__prenom",
    )

    autocomplete_fields = (
        "Eleve",
        "book",
    )

    readonly_fields = (
        "issue_date",
    )


# ==========================================================
# RECOMMANDATIONS
# ==========================================================

@admin.register(LibraryRecommendation)
class LibraryRecommendationAdmin(admin.ModelAdmin):

    list_display = (
        "Eleve",
        "recommended_book",
        "confidence",
        "accepted",
    )

    search_fields = (
        "Eleve__nom",
        "Eleve__prenom",
        "recommended_book__title",
    )

    autocomplete_fields = (
        "Eleve",
        "recommended_book",
    )


# ==========================================================
# STATISTIQUES
# ==========================================================

@admin.register(LibraryStatistics)
class LibraryStatisticsAdmin(admin.ModelAdmin):

    list_display = (
        "book",
        "total_Eleves",
        "completed_Eleves",
        "average_progress",
        "average_rating",
        "success_rate",
    )

    search_fields = (
        "book__title",
    )

    readonly_fields = (
        "book",
        "total_Eleves",
        "completed_Eleves",
        "average_progress",
        "average_rating",
        "success_rate",
    )