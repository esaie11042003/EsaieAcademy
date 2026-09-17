
"""
==========================================================
                ADMINISTRATION DU CORE
==========================================================
 
Application : Core
Projet : Esaïe Academy
 
Ce fichier configure toute l'administration Django
des modèles de l'application Core.
 
Objectifs :
 
- Interface professionnelle
- Administration claire
- Recherche rapide
- Filtres avancés
- Badges colorés
- Actions de masse
- Sécurité
- Haute maintenabilité
 
==========================================================
"""
 
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
 
from .models import (
    ActivityLog,
    Notification,
    DashboardStatistic,
    PlatformSettings,
    FeatureFlag,
    SystemAnnouncement,
)
 
# ==========================================================
#                PERSONNALISATION DE L'ADMIN
# ==========================================================
 
admin.site.site_header = "Administration Esaïe Academy"
admin.site.site_title = "Esaïe Academy"
admin.site.index_title = "Tableau de bord"
 
# ==========================================================
#                 FONCTIONS UTILITAIRES
# ==========================================================
 
def colored_boolean(value):
    """
    Affiche un badge coloré Oui / Non.
    """
 
    if value:
        color = "#28a745"
        label = "OUI"
    else:
        color = "#dc3545"
        label = "NON"
 
    return format_html(
        """
        <span style="
            background:{};
            color:white;
            padding:4px 10px;
            border-radius:6px;
            font-weight:bold;
        ">
            {}
        </span>
        """,
        color,
        label,
    )
 
 
def colored_status(status):
    """
    Affiche un badge coloré selon le statut.
    """
 
    colors = {
        "draft": "#6c757d",
        "scheduled": "#17a2b8",
        "published": "#28a745",
        "archived": "#ffc107",
        "expired": "#dc3545",
        "success": "#28a745",
        "failed": "#dc3545",
        "pending": "#fd7e14",
    }
 
    color = colors.get(status, "#6c757d")
 
    return format_html(
        """
        <span style="
            background:{};
            color:white;
            padding:4px 10px;
            border-radius:6px;
            font-weight:bold;
        ">
            {}
        </span>
        """,
        color,
        str(status).upper(),
    )
 
 
def colored_priority(priority):
    """
    Badge de priorité.
    """
 
    colors = {
        "low": "#20c997",
        "normal": "#0d6efd",
        "high": "#fd7e14",
        "critical": "#dc3545",
    }
 
    color = colors.get(priority, "#6c757d")
 
    return format_html(
        """
        <span style="
            background:{};
            color:white;
            padding:4px 10px;
            border-radius:6px;
            font-weight:bold;
        ">
            {}
        </span>
        """,
        color,
        str(priority).upper(),
    )
 
# ==========================================================
#                    BASE ADMIN
# ==========================================================
 
class BaseAdmin(admin.ModelAdmin):
    """
    Classe de base utilisée par tous les ModelAdmin.
    """
 
    list_per_page = 50
 
    save_on_top = True
 
    actions_on_top = True
 
    actions_on_bottom = True
 
    show_full_result_count = True
    # ==========================================================
#                 ACTIVITY LOG ADMIN
# ==========================================================
 
@admin.register(ActivityLog)
class ActivityLogAdmin(BaseAdmin):
    """
    Administration du journal des activités.
 
    Toutes les actions importantes réalisées sur la plateforme
    sont enregistrées ici afin de faciliter :
 
    • les audits
    • la sécurité
    • le support technique
    • le suivi des utilisateurs
    """
 
    # ======================================================
    # LISTE
    # ======================================================
 
    list_display = (
        "user",
        "action",
        "school",
        "device_type",
        "browser",
        "ip_address",
        "status_badge",
        "created_at",
    )
 
    list_select_related = (
        "user",
        "school",
    )
 
    # ======================================================
    # FILTRES
    # ======================================================
 
    list_filter = (
        "action",
        "login_status",
        "device_type",
        "browser",
        "school",
        "country",
        "created_at",
    )
 
    date_hierarchy = "created_at"
 
    # ======================================================
    # RECHERCHE
    # ======================================================
 
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "ip_address",
        "browser",
        "device_type",
        "city",
        "country",
        "action",
    )
 
    ordering = (
        "-created_at",
    )
 
    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )
 
    # ======================================================
    # ORGANISATION
    # ======================================================
 
    fieldsets = (
 
        (
            "Informations générales",
            {
                "fields": (
                    "uuid",
                    "user",
                    "school",
                    "action",
                    "description",
                    "login_status",
                )
            },
        ),
 
        (
            "Informations techniques",
            {
                "fields": (
                    "ip_address",
                    "browser",
                    "device_type",
                    "operating_system",
                    "screen_resolution",
                    "browser_language",
                    "session_id",
                )
            },
        ),
 
        (
            "Localisation",
            {
                "classes": ("collapse",),
                "fields": (
                    "city",
                    "country",
                )
            },
        ),
 
        (
            "Informations complémentaires",
            {
                "classes": ("collapse",),
                "fields": (
                    "extra_data",
                )
            },
        ),
 
        (
            "Horodatage",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
 
    # ======================================================
    # BADGES
    # ======================================================
 
    @admin.display(description="Statut de connexion")
    def status_badge(self, obj):
        return colored_status(obj.login_status)
 
    # ======================================================
    # ACTIONS
    # ======================================================
 
    actions = (
        "mark_success",
        "mark_failed",
    )
 
    @admin.action(description="Marquer comme succès")
    def mark_success(self, request, queryset):
        queryset.update(login_status="success")
 
    @admin.action(description="Marquer comme échec")
    def mark_failed(self, request, queryset):
        queryset.update(login_status="failed")
 
    # ======================================================
    # PERMISSIONS
    # ======================================================
 
    def has_add_permission(self, request):
        """
        Les ActivityLog sont créés automatiquement.
        """
        return False
 
    def has_delete_permission(self, request, obj=None):
        """
        Seul le superutilisateur peut supprimer un journal.
        """
        return request.user.is_superuser
    # ==========================================================
#                 NOTIFICATION ADMIN
# ==========================================================
 
@admin.register(Notification)
class NotificationAdmin(BaseAdmin):
    """
    Administration des notifications de la plateforme.
    """
 
    # ======================================================
    # LISTE
    # ======================================================
 
    list_display = (
        "title",
        "school",
        "recipient",
        "notification_type",
        "priority_badge",
        "status_badge",
        "read_badge",
        "active_badge",
        "created_at",
    )
 
    list_select_related = (
        "school",
        "sender",
        "recipient",
    )
 
    # ======================================================
    # FILTRES
    # ======================================================
 
    list_filter = (
        "notification_type",
        "priority",
        "status",
        "is_read",
        "active",
        "school",
        "created_at",
    )
 
    date_hierarchy = "created_at"
 
    # ======================================================
    # RECHERCHE
    # ======================================================
 
    search_fields = (
        "title",
        "message",
        "description",
        "recipient__username",
        "recipient__first_name",
        "recipient__last_name",
        "sender__username",
    )
 
    ordering = (
        "-created_at",
    )
 
    # ======================================================
    # CHAMPS EN LECTURE SEULE
    # ======================================================
 
    readonly_fields = (
        "uuid",
        "sent_count",
        "read_count",
        "failed_count",
        "read_rate",
        "created_at",
        "updated_at",
    )
 
    # ======================================================
    # ORGANISATION
    # ======================================================
 
    fieldsets = (
 
        (
            "Informations générales",
            {
                "fields": (
                    "uuid",
                    "school",
                    "sender",
                    "recipient",
                    "recipients",
                    "classes",
                )
            },
        ),
 
        (
            "Contenu",
            {
                "fields": (
                    "title",
                    "message",
                    "description",
                    "notification_type",
                    "priority",
                )
            },
        ),
 
        (
            "Canaux d'envoi",
            {
                "classes": ("collapse",),
                "fields": (
                    "send_in_app",
                    "send_email",
                    "send_sms",
                    "send_whatsapp",
                    "send_push",
                )
            },
        ),
 
        (
            "Public cible",
            {
                "classes": ("collapse",),
                "fields": (
                    "send_to_students",
                    "send_to_teachers",
                    "send_to_staff",
                    "send_to_admins",
                    "send_to_school",
                    "send_to_platform",
                )
            },
        ),
 
        (
            "Programmation",
            {
                "fields": (
                    "scheduled_at",
                    "expires_at",
                    "status",
                    "is_read",
                    "read_at",
                    "active",
                )
            },
        ),
 
        (
            "Statistiques",
            {
                "classes": ("collapse",),
                "fields": (
                    "sent_count",
                    "read_count",
                    "failed_count",
                    "read_rate",
                )
            },
        ),
 
        (
            "Pièces jointes",
            {
                "classes": ("collapse",),
                "fields": (
                    "image",
                    "attachment",
                    "external_link",
                    "action_label",
                    "action_url",
                )
            },
        ),
 
        (
            "Métadonnées",
            {
                "classes": ("collapse",),
                "fields": (
                    "extra_data",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
 
    # ======================================================
    # BADGES
    # ======================================================
 
    @admin.display(description="Priorité")
    def priority_badge(self, obj):
        return colored_priority(obj.priority)
 
    @admin.display(description="Statut")
    def status_badge(self, obj):
        return colored_status(obj.status)
 
    @admin.display(description="Lue")
    def read_badge(self, obj):
        return colored_boolean(obj.is_read)
 
    @admin.display(description="Active")
    def active_badge(self, obj):
        return colored_boolean(obj.active)
 
    # ======================================================
    # ACTIONS
    # ======================================================
 
    actions = (
        "mark_as_read",
        "mark_as_unread",
        "activate_notifications",
        "deactivate_notifications",
    )
 
    @admin.action(description="Marquer comme lues")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
 
    @admin.action(description="Marquer comme non lues")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
 
    @admin.action(description="Activer les notifications")
    def activate_notifications(self, request, queryset):
        queryset.update(active=True)
 
    @admin.action(description="Désactiver les notifications")
    def deactivate_notifications(self, request, queryset):
        queryset.update(active=False)
        # ==========================================================
#             DASHBOARD STATISTIC ADMIN
# ==========================================================
 
@admin.register(DashboardStatistic)
class DashboardStatisticAdmin(BaseAdmin):
    """
    Administration des instantanés de statistiques
    (élèves, enseignants, finances, plateforme...)
    utilisés pour alimenter le tableau de bord.
    """
 
    # ======================================================
    # LISTE
    # ======================================================
 
    list_display = (
        "school",
        "statistic_type",
        "statistic_date",
        "total_students",
        "total_teachers",
        "average_score",
        "success_rate",
        "active_badge",
        "updated_at",
    )
 
    list_select_related = (
        "school",
        "school_year",
        "period",
    )
 
    # ======================================================
    # FILTRES
    # ======================================================
 
    list_filter = (
        "statistic_type",
        "school",
        "school_year",
        "period",
        "active",
        "statistic_date",
    )
 
    date_hierarchy = "statistic_date"
 
    # ======================================================
    # RECHERCHE
    # ======================================================
 
    search_fields = (
        "school__nom",
    )
 
    ordering = (
        "-statistic_date",
        "-created_at",
    )
 
    # ======================================================
    # CHAMPS EN LECTURE SEULE
    # ======================================================
 
    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )
 
    # ======================================================
    # ORGANISATION
    # ======================================================
 
    fieldsets = (
 
        (
            "Informations générales",
            {
                "fields": (
                    "uuid",
                    "school",
                    "school_year",
                    "period",
                    "statistic_type",
                    "statistic_date",
                )
            },
        ),
 
        (
            "Élèves",
            {
                "fields": (
                    "total_students",
                    "boys",
                    "girls",
                    "new_students",
                    "former_students",
                )
            },
        ),
 
        (
            "Enseignants et personnel",
            {
                "fields": (
                    "total_teachers",
                    "active_teachers",
                    "unavailable_teachers",
                    "total_staff",
                )
            },
        ),
 
        (
            "Classes et matières",
            {
                "fields": (
                    "total_classes",
                    "active_classes",
                    "total_subjects",
                )
            },
        ),
 
        (
            "Évaluations et bulletins",
            {
                "fields": (
                    "total_evaluations",
                    "completed_evaluations",
                    "generated_reports",
                    "printed_reports",
                    "downloaded_reports",
                )
            },
        ),
 
        (
            "Documents et utilisateurs",
            {
                "classes": ("collapse",),
                "fields": (
                    "uploaded_documents",
                    "downloaded_documents",
                    "total_users",
                    "online_users",
                    "active_sessions",
                )
            },
        ),
 
        (
            "Résultats pédagogiques",
            {
                "classes": ("collapse",),
                "fields": (
                    "average_score",
                    "highest_average",
                    "lowest_average",
                    "success_rate",
                    "failure_rate",
                    "attendance_rate",
                    "absence_rate",
                    "admitted_students",
                    "repeating_students",
                    "transferred_students",
                    "excluded_students",
                )
            },
        ),
 
        (
            "Finances",
            {
                "classes": ("collapse",),
                "fields": (
                    "total_expected_fees",
                    "total_paid_fees",
                    "total_remaining_fees",
                    "successful_payments",
                    "pending_payments",
                    "failed_payments",
                    "scholarship_students",
                    "discounted_students",
                )
            },
        ),
 
        (
            "Plateforme",
            {
                "classes": ("collapse",),
                "fields": (
                    "total_connections",
                    "unique_visitors",
                    "generated_notifications",
                    "downloaded_files",
                    "generated_reports_total",
                    "recorded_activities",
                )
            },
        ),
 
        (
            "Informations complémentaires",
            {
                "classes": ("collapse",),
                "fields": (
                    "extra_data",
                    "active",
                )
            },
        ),
 
        (
            "Horodatage",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
 
    # ======================================================
    # BADGES
    # ======================================================
 
    @admin.display(description="Actif")
    def active_badge(self, obj):
        return colored_boolean(obj.active)
 
    # ======================================================
    # ACTIONS
    # ======================================================
 
    actions = (
        "activate_statistics",
        "deactivate_statistics",
    )
 
    @admin.action(description="Activer les statistiques sélectionnées")
    def activate_statistics(self, request, queryset):
        queryset.update(active=True)
 
    @admin.action(description="Désactiver les statistiques sélectionnées")
    def deactivate_statistics(self, request, queryset):
        queryset.update(active=False)
        # ==========================================================
#              PLATFORM SETTINGS ADMIN
# ==========================================================
 
@admin.register(PlatformSettings)
class PlatformSettingsAdmin(BaseAdmin):
    """
    Administration des paramètres généraux de la plateforme.
 
    Une seule configuration doit normalement exister.
    """
 
    # ======================================================
    # LISTE
    # ======================================================
 
    list_display = (
        "platform_name",
        "license_type",
        "default_language",
        "default_currency",
        "active_badge",
        "updated_at",
    )
 
    # ======================================================
    # FILTRES
    # ======================================================
 
    list_filter = (
        "license_type",
        "default_language",
        "default_currency",
        "active",
        "enable_statistics_dashboard",
    )
 
    search_fields = (
        "platform_name",
        "description",
        "support_email",
        "support_phone",
    )
 
    ordering = (
        "platform_name",
    )
 
    # ======================================================
    # CHAMPS EN LECTURE SEULE
    # ======================================================
 
    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )
 
    # ======================================================
    # ORGANISATION
    # ======================================================
 
    fieldsets = (
 
        (
            "Informations générales",
            {
                "fields": (
                    "uuid",
                    "platform_name",
                    "description",
                    "logo",
                    "favicon",
                )
            },
        ),
 
        (
            "Contact",
            {
                "fields": (
                    "support_email",
                    "support_phone",
                    "website",
                )
            },
        ),
 
        (
            "Paramètres régionaux",
            {
                "fields": (
                    "default_language",
                    "default_timezone",
                    "default_currency",
                    "date_format",
                )
            },
        ),
 
        (
            "Licence",
            {
                "fields": (
                    "license_type",
                    "license_start",
                    "license_end",
                )
            },
        ),
 
        (
            "Fonctionnalités principales",
            {
                "classes": ("collapse",),
                "fields": (
                    "enable_pdf_export",
                    "enable_excel_export",
                    "enable_qr_code",
                    "enable_barcode",
                    "enable_electronic_signature",
                    "enable_online_payments",
                    "enable_download_center",
                    "enable_online_results",
                    "enable_online_report_cards",
                )
            },
        ),
 
        (
            "Communication",
            {
                "classes": ("collapse",),
                "fields": (
                    "enable_email_notifications",
                    "enable_sms_notifications",
                    "enable_whatsapp_notifications",
                    "enable_push_notifications",
                )
            },
        ),
 
        (
            "Sécurité",
            {
                "classes": ("collapse",),
                "fields": (
                    "enable_activity_logs",
                    "enable_auto_backup",
                    "enable_api",
                )
            },
        ),
 
        (
            "Tableau de bord",
            {
                "classes": ("collapse",),
                "fields": (
                    "enable_statistics_dashboard",
                )
            },
        ),
 
        (
            "Informations complémentaires",
            {
                "classes": ("collapse",),
                "fields": (
                    "extra_data",
                    "active",
                )
            },
        ),
 
        (
            "Horodatage",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
 
    )
 
    # ======================================================
    # BADGES
    # ======================================================
 
    @admin.display(description="Active")
    def active_badge(self, obj):
        return colored_boolean(obj.active)
 
    # ======================================================
    # EMPÊCHER PLUSIEURS CONFIGURATIONS
    # ======================================================
 
    def has_add_permission(self, request):
        """
        Une seule configuration globale est autorisée.
        """
        return not PlatformSettings.objects.exists()
    # ==========================================================
#                 FEATURE FLAG ADMIN
# ==========================================================
 
@admin.register(FeatureFlag)
class FeatureFlagAdmin(BaseAdmin):
    """
    Administration des fonctionnalités activables
    de la plateforme Esaïe Academy.
 
    Permet d'activer ou désactiver certaines
    fonctionnalités sans modifier le code.
    """
 
    # ======================================================
    # LISTE
    # ======================================================
 
    list_display = (
        "name",
        "code",
        "category",
        "school",
        "minimum_license",
        "enabled_badge",
        "beta_badge",
        "experimental_badge",
        "active_badge",
        "updated_at",
    )
 
    list_select_related = (
        "school",
    )
 
    # ======================================================
    # FILTRES
    # ======================================================
 
    list_filter = (
        "category",
        "enabled",
        "is_beta",
        "is_experimental",
        "minimum_license",
        "available_for_platform",
        "available_for_school",
        "school",
    )
 
    date_hierarchy = "updated_at"
 
    # ======================================================
    # RECHERCHE
    # ======================================================
 
    search_fields = (
        "name",
        "code",
        "description",
        "required_role",
        "required_permission",
        "required_group",
    )
 
    ordering = (
        "category",
        "display_order",
        "name",
    )
 
    # ======================================================
    # CHAMPS EN LECTURE SEULE
    # ======================================================
 
    readonly_fields = (
        "uuid",
        "is_active",
        "created_at",
        "updated_at",
    )
 
    # ======================================================
    # ORGANISATION
    # ======================================================
 
    fieldsets = (
 
        (
            "Informations générales",
            {
                "fields": (
                    "uuid",
                    "name",
                    "code",
                    "description",
                    "category",
                )
            },
        ),
 
        (
            "Disponibilité",
            {
                "fields": (
                    "enabled",
                    "available_for_platform",
                    "available_for_school",
                    "school",
                )
            },
        ),
 
        (
            "Licence",
            {
                "fields": (
                    "minimum_license",
                    "minimum_platform_version",
                )
            },
        ),
 
        (
            "Sécurité",
            {
                "classes": ("collapse",),
                "fields": (
                    "required_role",
                    "required_permission",
                    "required_group",
                )
            },
        ),
 
        (
            "Cycle de vie",
            {
                "fields": (
                    "starts_at",
                    "expires_at",
                    "is_beta",
                    "is_experimental",
                    "is_active",
                )
            },
        ),
 
        (
            "Organisation",
            {
                "fields": (
                    "display_order",
                    "extra_data",
                )
            },
        ),
 
        (
            "Horodatage",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
 
    )
 
    # ======================================================
    # BADGES
    # ======================================================
 
    @admin.display(description="Activée")
    def enabled_badge(self, obj):
        return colored_boolean(obj.enabled)
 
    @admin.display(description="Bêta")
    def beta_badge(self, obj):
        return colored_boolean(obj.is_beta)
 
    @admin.display(description="Expérimentale")
    def experimental_badge(self, obj):
        return colored_boolean(obj.is_experimental)
 
    @admin.display(description="Disponible")
    def active_badge(self, obj):
        return colored_boolean(obj.is_active)
 
    # ======================================================
    # ACTIONS
    # ======================================================
 
    actions = (
        "enable_features",
        "disable_features",
        "mark_beta",
        "unmark_beta",
        "mark_experimental",
        "unmark_experimental",
    )
 
    @admin.action(description="Activer les fonctionnalités")
    def enable_features(self, request, queryset):
        queryset.update(enabled=True)
 
    @admin.action(description="Désactiver les fonctionnalités")
    def disable_features(self, request, queryset):
        queryset.update(enabled=False)
 
    @admin.action(description="Passer en version bêta")
    def mark_beta(self, request, queryset):
        queryset.update(is_beta=True)
 
    @admin.action(description="Retirer du mode bêta")
    def unmark_beta(self, request, queryset):
        queryset.update(is_beta=False)
 
    @admin.action(description="Passer en mode expérimental")
    def mark_experimental(self, request, queryset):
        queryset.update(is_experimental=True)
 
    @admin.action(description="Retirer du mode expérimental")
    def unmark_experimental(self, request, queryset):
        queryset.update(is_experimental=False)
        # ==========================================================
#             SYSTEM ANNOUNCEMENT ADMIN
# ==========================================================
 
@admin.register(SystemAnnouncement)
class SystemAnnouncementAdmin(BaseAdmin):
    """
    Administration des annonces système.
 
    Les annonces peuvent être affichées sur
    toute la plateforme ou uniquement dans
    un établissement.
    """
 
    # ======================================================
    # LISTE
    # ======================================================
 
    list_display = (
        "title",
        "school",
        "announcement_type",
        "priority_badge",
        "status_badge",
        "pinned_badge",
        "banner_badge",
        "active_badge",
        "starts_at",
    )
 
    list_select_related = (
        "school",
        "created_by",
    )
 
    # ======================================================
    # FILTRES
    # ======================================================
 
    list_filter = (
        "announcement_type",
        "priority",
        "status",
        "active",
        "is_pinned",
        "show_as_banner",
        "school",
        "starts_at",
    )
 
    date_hierarchy = "starts_at"
 
    # ======================================================
    # RECHERCHE
    # ======================================================
 
    search_fields = (
        "title",
        "message",
        "description",
        "created_by__username",
        "school__nom",
    )
 
    ordering = (
        "-is_pinned",
        "-priority",
        "-starts_at",
    )
 
    # ======================================================
    # CHAMPS EN LECTURE SEULE
    # ======================================================
 
    readonly_fields = (
        "uuid",
        "views",
        "clicks",
        "click_rate",
        "email_sent",
        "sms_sent",
        "whatsapp_sent",
        "push_sent",
        "created_at",
        "updated_at",
    )
 
    # ======================================================
    # ORGANISATION
    # ======================================================
 
    fieldsets = (
 
        (
            "Informations générales",
            {
                "fields": (
                    "uuid",
                    "school",
                    "created_by",
                    "title",
                    "message",
                    "description",
                )
            },
        ),
 
        (
            "Classification",
            {
                "fields": (
                    "announcement_type",
                    "priority",
                    "status",
                )
            },
        ),
 
        (
            "Planification",
            {
                "fields": (
                    "starts_at",
                    "ends_at",
                    "active",
                )
            },
        ),
 
        (
            "Affichage",
            {
                "fields": (
                    "is_pinned",
                    "show_as_banner",
                    "show_on_homepage",
                    "show_on_dashboard",
                )
            },
        ),
 
        (
            "Canaux de diffusion",
            {
                "classes": ("collapse",),
                "fields": (
                    "show_as_notification",
                    "send_by_email",
                    "send_by_sms",
                    "send_by_whatsapp",
                    "send_as_push",
                )
            },
        ),
 
        (
            "Public concerné",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_global",
                    "visible_to_students",
                    "visible_to_teachers",
                    "visible_to_staff",
                    "visible_to_parents",
                )
            },
        ),
 
        (
            "Média",
            {
                "classes": ("collapse",),
                "fields": (
                    "image",
                    "attachment",
                    "external_url",
                    "action_label",
                    "action_url",
                )
            },
        ),
 
        (
            "Statistiques",
            {
                "classes": ("collapse",),
                "fields": (
                    "views",
                    "clicks",
                    "click_rate",
                    "email_sent",
                    "sms_sent",
                    "whatsapp_sent",
                    "push_sent",
                )
            },
        ),
 
        (
            "Options avancées",
            {
                "classes": ("collapse",),
                "fields": (
                    "require_acknowledgement",
                    "extra_data",
                )
            },
        ),
 
        (
            "Horodatage",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
 
    # ======================================================
    # BADGES
    # ======================================================
 
    @admin.display(description="Priorité")
    def priority_badge(self, obj):
        return colored_priority(obj.priority)
 
    @admin.display(description="Statut")
    def status_badge(self, obj):
        return colored_status(obj.status)
 
    @admin.display(description="Épinglée")
    def pinned_badge(self, obj):
        return colored_boolean(obj.is_pinned)
 
    @admin.display(description="Bandeau")
    def banner_badge(self, obj):
        return colored_boolean(obj.show_as_banner)
 
    @admin.display(description="Active")
    def active_badge(self, obj):
        return colored_boolean(obj.active)
 
    # ======================================================
    # ACTIONS
    # ======================================================
 
    actions = (
        "publish_announcements",
        "archive_announcements",
        "pin_announcements",
        "unpin_announcements",
        "activate_announcements",
        "deactivate_announcements",
    )
 
    @admin.action(description="Publier les annonces")
    def publish_announcements(self, request, queryset):
        queryset.update(status="published")
 
    @admin.action(description="Archiver les annonces")
    def archive_announcements(self, request, queryset):
        queryset.update(status="archived")
 
    @admin.action(description="Épingler les annonces")
    def pin_announcements(self, request, queryset):
        queryset.update(is_pinned=True)
 
    @admin.action(description="Retirer les annonces épinglées")
    def unpin_announcements(self, request, queryset):
        queryset.update(is_pinned=False)
 
    @admin.action(description="Activer")
    def activate_announcements(self, request, queryset):
        queryset.update(active=True)
 
    @admin.action(description="Désactiver")
    def deactivate_announcements(self, request, queryset):
        queryset.update(active=False)




