"""
==========================================================
                    ADMIN - PAYMENTS
==========================================================

Application : Payments
Projet : ESAIE ACADEMY

Administration complète de :

✔ Méthodes de paiement
✔ Références de paiement
✔ Passerelles de paiement
✔ Transactions
✔ Paiements scolaires
✔ Paiements par tranche
✔ Factures
✔ Reçus
✔ Caisses des écoles
✔ Sessions de caisse
✔ Remboursements
✔ Vérifications
✔ Journal d'audit
✔ Détection de fraude
✔ QR Codes
✔ Abonnements Premium (plateforme)
✔ Achats plateforme
✔ Licences d'accès
✔ Statistiques financières
✔ Webhooks
✔ Notifications
✔ Grand livre comptable

Compatible Django 6.x

==========================================================
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import (
    PaymentMethod,
    PaymentReference,
    PaymentGateway,
    PaymentTransaction,
    Invoice,
    Receipt,
    SchoolCashRegister,
    CashSession,
    SchoolPayment,
    PaymentInstallment,
    Refund,
    PaymentVerification,
    PaymentAuditLog,
    FraudDetection,
    QRCodeVerification,
    PlatformSubscription,
    PlatformPurchase,
    AccessLicense,
    PaymentStatistic,
    PaymentWebhook,
    PaymentNotification,
    LedgerEntry,
)


def _badge(text, color):
    return format_html(
        '<span style="color:white;background:{};'
        'padding:4px 10px;border-radius:8px;">{}</span>',
        color,
        text,
    )


# ==========================================================
#               MÉTHODES DE PAIEMENT
# ==========================================================

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    """
    Administration des méthodes de paiement.

    Exemples :
        • Espèces
        • MTN Mobile Money
        • Moov Money
        • Celtiis Money
        • Carte bancaire
        • Virement bancaire
    """

    list_display = (
        "name",
        "payment_type",
        "active_badge",
        "display_order",
    )

    search_fields = (
        "name",
        "description",
    )

    list_filter = (
        "payment_type",
        "active",
    )

    ordering = (
        "display_order",
        "name",
    )

    list_editable = (
        "display_order",
    )

    list_per_page = 25

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Informations générales", {
            "fields": (
                "name",
                "payment_type",
                "description",
            )
        }),
        ("Configuration", {
            "fields": (
                "active",
                "display_order",
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
#           RÉFÉRENCES DE PAIEMENT
# ==========================================================

@admin.register(PaymentReference)
class PaymentReferenceAdmin(admin.ModelAdmin):
    """
    Administration des références de paiement.

    Chaque paiement possède :
        • une référence unique
        • un numéro de reçu
        • un code de vérification
    """

    list_display = (
        "reference",
        "receipt_number",
        "verification_code",
        "year",
        "sequence",
        "created_at",
    )

    search_fields = (
        "reference",
        "receipt_number",
        "verification_code",
    )

    list_filter = (
        "year",
        "created_at",
    )

    ordering = (
        "-year",
        "-sequence",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "reference",
        "receipt_number",
        "verification_code",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Références sécurisées", {
            "fields": (
                "reference",
                "receipt_number",
                "verification_code",
            )
        }),
        ("Numérotation", {
            "fields": (
                "year",
                "sequence",
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
#              PASSERELLES DE PAIEMENT
# ==========================================================

@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    """
    Administration des passerelles de paiement
    (MTN Mobile Money, Moov Money, Celtiis Money,
    CinetPay, Kkiapay, Stripe, PayPal...).
    """

    list_display = (
        "name",
        "code",
        "sandbox_badge",
        "active_badge",
    )

    search_fields = (
        "name",
        "code",
    )

    list_filter = (
        "active",
        "sandbox_mode",
    )

    ordering = (
        "name",
    )

    list_per_page = 25

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
        ("Configuration API", {
            "classes": ("collapse",),
            "fields": (
                "api_url",
                "api_key",
                "secret_key",
                "webhook_secret",
            )
        }),
        ("État", {
            "fields": (
                "sandbox_mode",
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

    @admin.display(description="Mode")
    def sandbox_badge(self, obj):
        return _badge("Test", "#ffc107") if obj.sandbox_mode else _badge("Production", "#17a2b8")

    @admin.display(description="Statut")
    def active_badge(self, obj):
        return _badge("Active", "#28a745") if obj.active else _badge("Inactive", "#dc3545")


# ==========================================================
#               TRANSACTIONS DE PAIEMENT
# ==========================================================

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    """
    Administration des transactions de paiement.
    """

    list_display = (
        "reference_display",
        "payer_name",
        "amount",
        "payment_method",
        "gateway",
        "status_badge",
        "payment_date",
    )

    search_fields = (
        "payment_reference__reference",
        "payer_name",
        "payer_email",
        "phone_number",
        "external_transaction_id",
    )

    list_filter = (
        "status",
        "payment_method",
        "gateway",
        "payment_date",
    )

    ordering = (
        "-payment_date",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Références", {
            "fields": (
                "payment_reference",
                "gateway",
            )
        }),
        ("Payeur", {
            "fields": (
                "payer_name",
                "payer_email",
                "phone_number",
            )
        }),
        ("Paiement", {
            "fields": (
                "payment_method",
                "amount",
                "currency",
                "status",
                "payment_date",
            )
        }),
        ("Informations techniques", {
            "classes": ("collapse",),
            "fields": (
                "external_transaction_id",
                "gateway_response",
                "failure_reason",
                "ip_address",
                "user_agent",
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

    @admin.display(description="Référence")
    def reference_display(self, obj):
        return obj.payment_reference.reference

    @admin.display(description="Statut")
    def status_badge(self, obj):
        colors = {
            "pending": "#ffc107",
            "processing": "#17a2b8",
            "success": "#28a745",
            "failed": "#dc3545",
            "cancelled": "#6c757d",
            "refunded": "#fd7e14",
        }
        return _badge(obj.get_status_display(), colors.get(obj.status, "#6c757d"))


# ==========================================================
#                     FACTURES
# ==========================================================

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Administration des factures.

    Une facture peut concerner les frais de scolarité,
    un document payant, un abonnement Premium, etc.
    """

    list_display = (
        "invoice_number",
        "title",
        "total_amount",
        "amount_paid",
        "remaining_amount",
        "status_badge",
        "issue_date",
        "due_date",
    )

    search_fields = (
        "invoice_number",
        "title",
    )

    list_filter = (
        "status",
        "issue_date",
        "due_date",
    )

    ordering = (
        "-issue_date",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "issue_date",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Informations générales", {
            "fields": (
                "invoice_number",
                "title",
                "description",
            )
        }),
        ("Facturation", {
            "fields": (
                "total_amount",
                "amount_paid",
                "remaining_amount",
                "status",
                "issue_date",
                "due_date",
            )
        }),
        ("Observations", {
            "fields": (
                "notes",
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
            "draft": "#6c757d",
            "pending": "#ffc107",
            "partial": "#17a2b8",
            "paid": "#28a745",
            "cancelled": "#dc3545",
        }
        return _badge(obj.get_status_display(), colors.get(obj.status, "#6c757d"))


# ==========================================================
#                     REÇUS
# ==========================================================

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    """
    Administration des reçus de paiement.
    """

    list_display = (
        "receipt_number",
        "payment",
        "amount",
        "issue_date",
        "valid_badge",
        "cancelled_badge",
    )

    search_fields = (
        "receipt_number",
        "verification_code",
        "payment__payment_reference__reference",
    )

    list_filter = (
        "issue_date",
        "is_valid",
        "cancelled",
    )

    ordering = (
        "-issue_date",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "issue_date",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Informations du reçu", {
            "fields": (
                "receipt_number",
                "payment",
                "invoice",
                "verification_code",
            )
        }),
        ("Informations financières", {
            "fields": (
                "amount",
                "issue_date",
            )
        }),
        ("Fichiers", {
            "fields": (
                "qr_code",
                "pdf_receipt",
            )
        }),
        ("État", {
            "fields": (
                "is_valid",
                "cancelled",
                "cancellation_reason",
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

    @admin.display(description="Valide")
    def valid_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.is_valid else _badge("Non", "#dc3545")

    @admin.display(description="Annulé")
    def cancelled_badge(self, obj):
        return _badge("Oui", "#dc3545") if obj.cancelled else _badge("Non", "#28a745")


# ==========================================================
#                  CAISSES DES ÉCOLES
# ==========================================================

@admin.register(SchoolCashRegister)
class SchoolCashRegisterAdmin(admin.ModelAdmin):
    """
    Administration des caisses des établissements.
    """

    list_display = (
        "name",
        "code",
        "opening_balance",
        "current_balance",
        "active_badge",
    )

    search_fields = (
        "name",
        "code",
    )

    list_filter = (
        "active",
    )

    ordering = (
        "name",
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
        ("Situation financière", {
            "fields": (
                "opening_balance",
                "current_balance",
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

    @admin.display(description="Active")
    def active_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.active else _badge("Non", "#dc3545")


# ==========================================================
#              SESSIONS DE CAISSE
# ==========================================================

@admin.register(CashSession)
class CashSessionAdmin(admin.ModelAdmin):
    """
    Administration des ouvertures et fermetures de caisse.
    """

    list_display = (
        "session_number",
        "cash_register",
        "opening_datetime",
        "opening_balance",
        "closing_balance",
        "status_badge",
    )

    search_fields = (
        "session_number",
        "cash_register__name",
    )

    list_filter = (
        "status",
        "opening_datetime",
    )

    ordering = (
        "-opening_datetime",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "opening_datetime",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Informations générales", {
            "fields": (
                "cash_register",
                "session_number",
            )
        }),
        ("Ouverture", {
            "fields": (
                "opening_datetime",
                "opening_balance",
            )
        }),
        ("Fermeture", {
            "fields": (
                "closing_datetime",
                "closing_balance",
            )
        }),
        ("Mouvements", {
            "fields": (
                "total_income",
                "total_expense",
            )
        }),
        ("État de la session", {
            "fields": (
                "status",
                "observations",
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
            "open": "#28a745",
            "closed": "#6c757d",
        }
        return _badge(obj.get_status_display(), colors.get(obj.status, "#6c757d"))


# ==========================================================
#               PAIEMENTS SCOLAIRES
# ==========================================================

@admin.register(SchoolPayment)
class SchoolPaymentAdmin(admin.ModelAdmin):
    """
    Administration des paiements des frais scolaires.
    """

    list_display = (
        "payment_reference",
        "invoice",
        "cash_session",
        "amount",
        "status_badge",
        "payment_date",
    )

    search_fields = (
        "payment_reference__reference",
        "invoice__invoice_number",
    )

    list_filter = (
        "status",
        "payment_date",
    )

    ordering = (
        "-payment_date",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "payment_date",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Références", {
            "fields": (
                "payment_reference",
                "invoice",
                "cash_session",
            )
        }),
        ("Paiement", {
            "fields": (
                "amount",
                "status",
                "payment_date",
            )
        }),
        ("Observations", {
            "fields": (
                "remarks",
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
            "partial": "#17a2b8",
            "paid": "#28a745",
            "cancelled": "#dc3545",
        }
        return _badge(obj.get_status_display(), colors.get(obj.status, "#6c757d"))


# ==========================================================
#               TRANCHES DE PAIEMENT
# ==========================================================

@admin.register(PaymentInstallment)
class PaymentInstallmentAdmin(admin.ModelAdmin):
    """
    Administration des paiements par tranche.
    """

    list_display = (
        "school_payment",
        "installment_number",
        "due_date",
        "expected_amount",
        "paid_amount",
        "status_badge",
    )

    search_fields = (
        "school_payment__payment_reference__reference",
    )

    list_filter = (
        "status",
        "due_date",
    )

    ordering = (
        "school_payment",
        "installment_number",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Paiement concerné", {
            "fields": (
                "school_payment",
            )
        }),
        ("Informations sur la tranche", {
            "fields": (
                "installment_number",
                "expected_amount",
                "paid_amount",
                "due_date",
                "payment_date",
                "status",
            )
        }),
        ("Observations", {
            "fields": (
                "observations",
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
            "paid": "#28a745",
            "late": "#dc3545",
        }
        return _badge(obj.get_status_display(), colors.get(obj.status, "#6c757d"))


# ==========================================================
#                REMBOURSEMENTS
# ==========================================================

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    """
    Historique des remboursements.
    """

    list_display = (
        "transaction",
        "amount",
        "status_badge",
        "refund_date",
    )

    search_fields = (
        "transaction__payment_reference__reference",
    )

    list_filter = (
        "status",
        "refund_date",
    )

    ordering = (
        "-refund_date",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "refund_date",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Transaction concernée", {
            "fields": (
                "transaction",
            )
        }),
        ("Remboursement", {
            "fields": (
                "amount",
                "reason",
                "status",
                "refund_date",
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
            "approved": "#17a2b8",
            "completed": "#28a745",
            "rejected": "#dc3545",
        }
        return _badge(obj.get_status_display(), colors.get(obj.status, "#6c757d"))


# ==========================================================
#            VÉRIFICATION DES PAIEMENTS
# ==========================================================

@admin.register(PaymentVerification)
class PaymentVerificationAdmin(admin.ModelAdmin):
    """
    Vérification officielle des paiements.
    """

    list_display = (
        "transaction",
        "verification_code",
        "status_badge",
        "verified_at",
    )

    search_fields = (
        "verification_code",
        "transaction__payment_reference__reference",
    )

    list_filter = (
        "status",
        "verified_at",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Transaction concernée", {
            "fields": (
                "transaction",
                "verification_code",
            )
        }),
        ("Résultat", {
            "fields": (
                "status",
                "verified_at",
                "notes",
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
            "verified": "#28a745",
            "rejected": "#dc3545",
        }
        return _badge(obj.get_status_display(), colors.get(obj.status, "#6c757d"))


# ==========================================================
#            JOURNAL DE SÉCURITÉ
# ==========================================================

@admin.register(PaymentAuditLog)
class PaymentAuditLogAdmin(admin.ModelAdmin):
    """
    Journal complet des opérations effectuées
    sur les paiements.
    """

    list_display = (
        "action",
        "performed_by",
        "transaction",
        "ip_address",
        "created_at",
    )

    search_fields = (
        "performed_by",
        "transaction__payment_reference__reference",
    )

    list_filter = (
        "action",
        "created_at",
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
                "transaction",
                "action",
                "performed_by",
                "ip_address",
            )
        }),
        ("Détails", {
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


# ==========================================================
#            DÉTECTION DE FRAUDE
# ==========================================================

@admin.register(FraudDetection)
class FraudDetectionAdmin(admin.ModelAdmin):
    """
    Détection automatique des opérations suspectes.
    """

    list_display = (
        "transaction",
        "level_badge",
        "resolved_badge",
        "resolved_at",
    )

    search_fields = (
        "transaction__payment_reference__reference",
        "detected_reason",
    )

    list_filter = (
        "level",
        "resolved",
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
        ("Transaction concernée", {
            "fields": (
                "transaction",
                "level",
            )
        }),
        ("Détails", {
            "fields": (
                "detected_reason",
                "resolved",
                "resolved_at",
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

    @admin.display(description="Niveau")
    def level_badge(self, obj):
        colors = {
            "low": "#28a745",
            "medium": "#ffc107",
            "high": "#fd7e14",
            "critical": "#dc3545",
        }
        return _badge(obj.get_level_display(), colors.get(obj.level, "#6c757d"))

    @admin.display(description="Résolu")
    def resolved_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.resolved else _badge("Non", "#dc3545")


# ==========================================================
#          VÉRIFICATION PAR QR CODE
# ==========================================================

@admin.register(QRCodeVerification)
class QRCodeVerificationAdmin(admin.ModelAdmin):
    """
    Vérification des reçus par QR Code.
    """

    list_display = (
        "receipt",
        "qr_token",
        "active_badge",
    )

    search_fields = (
        "qr_token",
        "receipt__receipt_number",
    )

    list_filter = (
        "active",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Reçu concerné", {
            "fields": (
                "receipt",
                "qr_token",
                "verification_url",
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

    @admin.display(description="Actif")
    def active_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.active else _badge("Non", "#dc3545")


# ==========================================================
#             ABONNEMENTS PREMIUM (PLATEFORME)
# ==========================================================

@admin.register(PlatformSubscription)
class PlatformSubscriptionAdmin(admin.ModelAdmin):
    """
    Catalogue des offres d'abonnement Premium
    de la plateforme (mensuel, trimestriel, etc.).
    """

    list_display = (
        "name",
        "duration",
        "price",
        "active_badge",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "duration",
        "active",
    )

    ordering = (
        "price",
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
                "duration",
                "price",
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

    @admin.display(description="Actif")
    def active_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.active else _badge("Non", "#dc3545")


# ==========================================================
#            ACHATS DE LA PLATEFORME
# ==========================================================

@admin.register(PlatformPurchase)
class PlatformPurchaseAdmin(admin.ModelAdmin):
    """
    Historique des achats effectués sur la plateforme
    (documents, vidéos, cours, examens, concours,
    abonnements, etc.).
    """

    list_display = (
        "title",
        "purchase_type",
        "amount",
        "payment_date",
        "active_badge",
    )

    search_fields = (
        "title",
        "payment_reference__reference",
    )

    list_filter = (
        "purchase_type",
        "active",
        "payment_date",
    )

    ordering = (
        "-payment_date",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "payment_date",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Achat", {
            "fields": (
                "payment_reference",
                "purchase_type",
                "title",
            )
        }),
        ("Paiement", {
            "fields": (
                "amount",
                "payment_date",
            )
        }),
        ("Accès", {
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

    @admin.display(description="Accès autorisé")
    def active_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.active else _badge("Non", "#dc3545")


# ==========================================================
#             LICENCES D'ACCÈS
# ==========================================================

@admin.register(AccessLicense)
class AccessLicenseAdmin(admin.ModelAdmin):
    """
    Licences d'accès générées après un achat plateforme.
    """

    list_display = (
        "access_key",
        "purchase",
        "start_date",
        "expiration_date",
        "active_badge",
    )

    search_fields = (
        "access_key",
        "purchase__title",
    )

    list_filter = (
        "active",
        "expiration_date",
    )

    ordering = (
        "-start_date",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "start_date",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Achat concerné", {
            "fields": (
                "purchase",
                "access_key",
            )
        }),
        ("Validité", {
            "fields": (
                "start_date",
                "expiration_date",
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

    @admin.display(description="Active")
    def active_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.active else _badge("Non", "#dc3545")


# ==========================================================
#             STATISTIQUES FINANCIÈRES
# ==========================================================

@admin.register(PaymentStatistic)
class PaymentStatisticAdmin(admin.ModelAdmin):
    """
    Statistiques financières alimentant le tableau
    de bord administrateur.
    """

    list_display = (
        "label",
        "value",
        "statistic_date",
    )

    search_fields = (
        "label",
    )

    list_filter = (
        "statistic_date",
    )

    ordering = (
        "-statistic_date",
        "label",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )


# ==========================================================
#          WEBHOOKS DE PAIEMENT
# ==========================================================

@admin.register(PaymentWebhook)
class PaymentWebhookAdmin(admin.ModelAdmin):
    """
    Historique des notifications envoyées
    par les opérateurs (MTN, Moov, Stripe...).
    """

    list_display = (
        "gateway",
        "event",
        "processed_badge",
        "created_at",
    )

    search_fields = (
        "event",
        "gateway__name",
    )

    list_filter = (
        "processed",
        "gateway",
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
        ("Origine", {
            "fields": (
                "gateway",
                "event",
            )
        }),
        ("Contenu", {
            "fields": (
                "payload",
                "processed",
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

    @admin.display(description="Traité")
    def processed_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.processed else _badge("Non", "#dc3545")


# ==========================================================
#          NOTIFICATIONS DE PAIEMENT
# ==========================================================

@admin.register(PaymentNotification)
class PaymentNotificationAdmin(admin.ModelAdmin):
    """
    Notifications envoyées aux utilisateurs
    après un paiement.
    """

    list_display = (
        "transaction",
        "channel",
        "recipient",
        "sent_badge",
        "sent_at",
    )

    search_fields = (
        "recipient",
        "transaction__payment_reference__reference",
    )

    list_filter = (
        "channel",
        "sent",
        "sent_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "sent_at",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Transaction concernée", {
            "fields": (
                "transaction",
                "channel",
                "recipient",
            )
        }),
        ("Message", {
            "fields": (
                "message",
            )
        }),
        ("Envoi", {
            "fields": (
                "sent",
                "sent_at",
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

    @admin.display(description="Envoyé")
    def sent_badge(self, obj):
        return _badge("Oui", "#28a745") if obj.sent else _badge("Non", "#dc3545")


# ==========================================================
#              GRAND LIVRE COMPTABLE
# ==========================================================

@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    """
    Grand livre comptable : chaque paiement validé
    génère automatiquement une écriture.
    """

    list_display = (
        "transaction",
        "entry_type_badge",
        "amount",
        "entry_date",
    )

    search_fields = (
        "transaction__payment_reference__reference",
        "description",
    )

    list_filter = (
        "entry_type",
        "entry_date",
    )

    ordering = (
        "-entry_date",
    )

    list_per_page = 30

    readonly_fields = (
        "uuid",
        "entry_date",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Écriture", {
            "fields": (
                "transaction",
                "entry_type",
                "amount",
                "description",
            )
        }),
        ("Informations système", {
            "classes": ("collapse",),
            "fields": (
                "uuid",
                "entry_date",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Type")
    def entry_type_badge(self, obj):
        color = "#28a745" if obj.entry_type == "credit" else "#dc3545"
        return _badge(obj.get_entry_type_display(), color)