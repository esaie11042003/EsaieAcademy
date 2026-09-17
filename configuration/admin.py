from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count

from .models import (
    SchoolProfile,
    StaffRole,
    SchoolStaff,
)


# ============================================================
#
#          FONCTIONS UTILITAIRES
#
# ============================================================

def image_preview(image, width=80):
    """
    Affiche une miniature d'une image dans Django Admin.
    """

    if image:
        return format_html(
            '<img src="{}" width="{}" '
            'style="border-radius:8px;border:1px solid #cccccc;" />',
            image.url,
            width
        )

    return "Aucune image"


# ============================================================
#
#          BADGE D'ÉTAT
#
# ============================================================

def status_badge(value):

    if value:

        color = "#198754"
        texte = "ACTIF"

    else:

        color = "#dc3545"
        texte = "INACTIF"

    return format_html(
        '<strong style="color:{};">{}</strong>',
        color,
        texte,
    )


# ============================================================
#
#          ACTIONS PERSONNALISÉES
#
# ============================================================

@admin.action(description="Activer les éléments sélectionnés")
def make_active(modeladmin, request, queryset):

    queryset.update(actif=True)


@admin.action(description="Désactiver les éléments sélectionnés")
def make_inactive(modeladmin, request, queryset):

    queryset.update(actif=False)


@admin.action(description="Afficher toutes les signatures")
def show_signature(modeladmin, request, queryset):

    queryset.update(afficher_signature=True)


@admin.action(description="Masquer toutes les signatures")
def hide_signature(modeladmin, request, queryset):

    queryset.update(afficher_signature=False)


# ============================================================
#
#          INLINE : FONCTIONS
#
# ============================================================
#
# Les fonctions seront directement visibles
# dans la fiche d'un établissement.
#
# Exemple :
#
# ESA001
#
#     Directeur
#     Censeur
#     Comptable
#
# ============================================================

class StaffRoleInline(admin.TabularInline):

    model = StaffRole

    extra = 1

    fields = (
        "nom",
        "ordre",
        "actif",
    )

    ordering = (
        "ordre",
    )

    show_change_link = True


# ============================================================
#
#          INLINE : RESPONSABLES
#
# ============================================================
#
# Les responsables apparaîtront directement
# dans la fiche de l'établissement.
#
# ============================================================

class SchoolStaffInline(admin.TabularInline):

    model = SchoolStaff

    extra = 0

    autocomplete_fields = (
        "user",
        "role",
    )

    fields = (
        "user",
        "role",
        "ordre_signature",
        "afficher_signature",
        "actif",
    )

    ordering = (
        "ordre_signature",
    )

    show_change_link = True
    # ============================================================
#
#          ADMINISTRATION : ÉTABLISSEMENT
#
# ============================================================

@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):

    # ========================================================
    # Colonnes affichées
    # ========================================================

    list_display = (
        "logo_preview",
        "nom",
        "sigle",
        "code_etablissement",
        "type_etablissement",
        "ville",
        "telephone",
        "nombre_fonctions",
        "nombre_responsables",
        "statut",
    )

    # ========================================================
    # Recherche
    # ========================================================

    search_fields = (
        "nom",
        "sigle",
        "code_etablissement",
        "ville",
        "telephone",
        "email",
    )

    # ========================================================
    # Filtres
    # ========================================================

    list_filter = (
        "type_etablissement",
        "ville",
        "actif",
    )

    # ========================================================
    # Tri
    # ========================================================

    ordering = (
        "nom",
    )

    # ========================================================
    # Pagination
    # ========================================================

    list_per_page = 20

    # ========================================================
    # Optimisation
    # ========================================================

    list_select_related = ()

    # ========================================================
    # Champs en lecture seule
    # ========================================================

    readonly_fields = (
        "slug",
        "logo_preview",
        "cover_preview",
        "created_at",
        "updated_at",
    )

    # ========================================================
    # Actions
    # ========================================================

    actions = (
        make_active,
        make_inactive,
    )

    # ========================================================
    # Inline
    # ========================================================

    inlines = (
        StaffRoleInline,
        SchoolStaffInline,
    )

    # ========================================================
    # Organisation du formulaire
    # ========================================================

    fieldsets = (

        (
            "Informations générales",
            {
                "fields": (
                    "code_etablissement",
                    "nom",
                    "sigle",
                    "slug",
                    "type_etablissement",
                    "devise",
                    "description",
                )
            }
        ),

        (
            "Images",
            {
                "fields": (
                    "logo",
                    "logo_preview",
                    "photo_couverture",
                    "cover_preview",
                )
            }
        ),

        (
            "Localisation",
            {
                "fields": (
                    "adresse",
                    "quartier",
                    "ville",
                    "departement",
                    "pays",
                )
            }
        ),

        (
            "Contacts",
            {
                "fields": (
                    "telephone",
                    "telephone_secondaire",
                    "whatsapp",
                    "email",
                    "site_web",
                )
            }
        ),

        (
            "Paramètres",
            {
                "fields": (
                    "subdomain",
                    "timezone",
                    "actif",
                )
            }
        ),

        (
            "Informations administratives",
            {
                "classes": ("collapse",),
                "fields": (
                    "date_creation",
                    "numero_autorisation",
                    "ifu",
                )
            }
        ),

        (
            "Historique",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),

    )

    # ========================================================
    # Aperçu du logo
    # ========================================================

    @admin.display(description="Logo")

    def logo_preview(self, obj):

        return image_preview(obj.logo)

    # ========================================================
    # Aperçu de la couverture
    # ========================================================

    @admin.display(description="Couverture")

    def cover_preview(self, obj):

        return image_preview(obj.photo_couverture, 140)

    # ========================================================
    # Badge Actif / Inactif
    # ========================================================

    @admin.display(description="Statut")

    def statut(self, obj):

        return status_badge(obj.actif)

    # ========================================================
    # Nombre de fonctions
    # ========================================================

    @admin.display(description="Fonctions")

    def nombre_fonctions(self, obj):

        return obj.roles.count()

    # ========================================================
    # Nombre de responsables
    # ========================================================

    @admin.display(description="Responsables")

    def nombre_responsables(self, obj):

        return obj.staff_members.count()
    # ============================================================
#
#          ADMINISTRATION : FONCTIONS
#
# ============================================================
#
# Cette administration permet de gérer toutes les fonctions
# d'un établissement.
#
# Exemples :
#
# • Directeur
# • Directeur adjoint
# • Censeur
# • Secrétaire
# • Comptable
# • Responsable informatique
#
# ============================================================

@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):

    # ========================================================
    # Colonnes affichées
    # ========================================================

    list_display = (
        "nom",
        "school",
        "ordre",
        "nombre_responsables",
        "statut",
    )

    # ========================================================
    # Recherche
    # ========================================================

    search_fields = (
        "nom",
        "description",
        "school__nom",
        "school__sigle",
    )

    # ========================================================
    # Filtres
    # ========================================================

    list_filter = (
        "school",
        "actif",
    )

    # ========================================================
    # Tri
    # ========================================================

    ordering = (
        "school",
        "ordre",
        "nom",
    )

    # ========================================================
    # Pagination
    # ========================================================

    list_per_page = 25

    # ========================================================
    # Optimisation des requêtes
    # ========================================================

    list_select_related = (
        "school",
    )

    # ========================================================
    # Actions disponibles
    # ========================================================

    actions = (
        make_active,
        make_inactive,
    )

    # ========================================================
    # Champs en lecture seule
    # ========================================================

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    # ========================================================
    # Organisation du formulaire
    # ========================================================

    fieldsets = (

        (
            "Informations générales",
            {
                "fields": (
                    "school",
                    "nom",
                    "description",
                )
            }
        ),

        (
            "Paramètres",
            {
                "fields": (
                    "ordre",
                    "actif",
                )
            }
        ),

        (
            "Historique",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),

    )

    # ========================================================
    # Badge Actif / Inactif
    # ========================================================

    @admin.display(description="Statut")

    def statut(self, obj):

        return status_badge(obj.actif)

    # ========================================================
    # Nombre de responsables utilisant cette fonction
    # ========================================================

    @admin.display(description="Responsables")

    def nombre_responsables(self, obj):

        return obj.staff.count()
    # ============================================================
#
#          ADMINISTRATION : RESPONSABLES
#
# ============================================================
#
# Cette administration permet de gérer les responsables
# d'un établissement scolaire.
#
# Les informations personnelles (nom, prénom, téléphone,
# email, photo...) proviennent automatiquement du modèle
# CustomUser.
#
# ============================================================

@admin.register(SchoolStaff)
class SchoolStaffAdmin(admin.ModelAdmin):

    # ========================================================
    # Colonnes affichées
    # ========================================================

    list_display = (
        "user_photo",
        "nom_complet",
        "school",
        "role",
        "telephone",
        "ordre_signature",
        "signature_preview",
        "statut",
    )

    # ========================================================
    # Recherche
    # ========================================================

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__phone",
        "school__nom",
        "role__nom",
    )

    # ========================================================
    # Filtres
    # ========================================================

    list_filter = (
        "school",
        "role",
        "actif",
        "afficher_signature",
    )

    # ========================================================
    # Optimisation
    # ========================================================

    list_select_related = (
        "user",
        "school",
        "role",
    )

    # ========================================================
    # Tri
    # ========================================================

    ordering = (
        "school",
        "ordre_signature",
        "role",
    )

    # ========================================================
    # Pagination
    # ========================================================

    list_per_page = 25

    # ========================================================
    # Actions
    # ========================================================

    actions = (
        make_active,
        make_inactive,
        show_signature,
        hide_signature,
    )

    # ========================================================
    # Lecture seule
    # ========================================================

    readonly_fields = (
        "user_photo_large",
        "signature_preview_large",
        "created_at",
        "updated_at",
    )

    # ========================================================
    # Auto-complétion
    # ========================================================

    autocomplete_fields = (
        "user",
        "school",
        "role",
    )

    # ========================================================
    # Organisation du formulaire
    # ========================================================

    fieldsets = (

        (
            "Affectation",
            {
                "fields": (
                    "school",
                    "user",
                    "role",
                )
            }
        ),

        (
            "Signature officielle",
            {
                "fields": (
                    "signature",
                    "signature_preview_large",
                    "ordre_signature",
                    "afficher_signature",
                )
            }
        ),

        (
            "Statut",
            {
                "fields": (
                    "actif",
                )
            }
        ),

        (
            "Compte utilisateur",
            {
                "classes": ("collapse",),

                "description":

                "Les informations personnelles "
                "proviennent automatiquement du "
                "compte utilisateur.",

                "fields": (
                    "user_photo_large",
                )

            }
        ),

        (
            "Historique",
            {
                "classes": ("collapse",),

                "fields": (
                    "created_at",
                    "updated_at",
                )

            }
        ),

    )

    # ========================================================
    # Nom complet
    # ========================================================

    @admin.display(description="Responsable")

    def nom_complet(self, obj):

        nom = obj.user.get_full_name()

        if nom:

            return nom

        return obj.user.username

    # ========================================================
    # Téléphone
    # ========================================================

    @admin.display(description="Téléphone")

    def telephone(self, obj):

        return obj.user.phone

    # ========================================================
    # Badge Actif / Inactif
    # ========================================================

    @admin.display(description="Statut")

    def statut(self, obj):

        return status_badge(obj.actif)

    # ========================================================
    # Petite photo
    # ========================================================

    @admin.display(description="Photo")

    def user_photo(self, obj):

        return image_preview(
            obj.user.profile_picture,
            45
        )

    # ========================================================
    # Grande photo
    # ========================================================

    @admin.display(description="Photo")

    def user_photo_large(self, obj):

        return image_preview(
            obj.user.profile_picture,
            140
        )

    # ========================================================
    # Petite signature
    # ========================================================

    @admin.display(description="Signature")

    def signature_preview(self, obj):

        return image_preview(
            obj.signature,
            90
        )

    # ========================================================
    # Grande signature
    # ========================================================

    @admin.display(description="Aperçu de la signature")

    def signature_preview_large(self, obj):

        return image_preview(
            obj.signature,
            220
        )