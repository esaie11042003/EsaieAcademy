"""
==========================================================
                MODELS - PAYMENTS
==========================================================

Application : Payments
Projet : Esaïe Academy

Cette application gère :

PARTIE A - Paiements des écoles
    - Frais de scolarité
    - Frais d'inscription
    - Paiements par tranche
    - Reçus
    - Factures
    - Caisses
    - Sessions de caisse

PARTIE B - Paiements de la plateforme
    - Documents payants
    - Abonnements Premium
    - Formations
    - Concours
    - Services additionnels

Le système est conçu pour être hautement sécurisé.
==========================================================
"""

import uuid
from django.db import models
from django.utils import timezone


# ==========================================================
#              CLASSE DE BASE
# ==========================================================

class BasePaymentModel(models.Model):
    """
    Classe abstraite utilisée par tous les modèles
    de paiement.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Identifiant unique"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Modifié le"
    )

    class Meta:
        abstract = True
        # ==========================================================
#              MÉTHODES DE PAIEMENT
# ==========================================================

class PaymentMethod(BasePaymentModel):
    """
    Liste des moyens de paiement disponibles.
    """

    TYPE_CHOICES = [
        ("cash", "Espèces"),
        ("mtn_momo", "MTN Mobile Money"),
        ("moov_money", "Moov Money"),
        ("celtiis_money", "Celtiis Money"),
        ("bank", "Virement bancaire"),
        ("card", "Carte bancaire"),
        ("check", "Chèque"),
        ("other", "Autre"),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la méthode"
    )

    payment_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        verbose_name="Type"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    display_order = models.PositiveIntegerField(
        default=1,
        verbose_name="Ordre d'affichage"
    )

    class Meta:
        verbose_name = "Méthode de paiement"
        verbose_name_plural = "Méthodes de paiement"
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name
    # ==========================================================
#              RÉFÉRENCES DE PAIEMENT
# ==========================================================

class PaymentReference(BasePaymentModel):
    """
    Génère des références uniques et sécurisées.

    Exemple :
        PAY-2026-00000125
        REC-2026-00000125
    """

    reference = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Référence"
    )

    receipt_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Numéro de reçu"
    )

    verification_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code de vérification"
    )

    year = models.PositiveIntegerField(
        default=timezone.now().year,
        verbose_name="Année"
    )

    sequence = models.PositiveIntegerField(
        verbose_name="Numéro de séquence"
    )

    class Meta:
        verbose_name = "Référence de paiement"
        verbose_name_plural = "Références de paiement"
        ordering = ["-year", "-sequence"]

    def __str__(self):
        return self.reference
# ==========================================================
#                 PASSERELLES DE PAIEMENT
# ==========================================================

class PaymentGateway(BasePaymentModel):
    """
    Représente une passerelle de paiement.

    Une passerelle est un fournisseur qui permet
    d'encaisser les paiements.

    Exemples :

    • MTN Mobile Money
    • Moov Money
    • Celtiis Money
    • CinetPay
    • Kkiapay
    • Stripe
    • PayPal
    """

    name = models.CharField(
        max_length=120,
        unique=True,
        verbose_name="Nom"
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code interne"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    api_url = models.URLField(
        blank=True,
        verbose_name="URL API"
    )

    api_key = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Clé API"
    )

    secret_key = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Clé secrète"
    )

    webhook_secret = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Webhook Secret"
    )

    sandbox_mode = models.BooleanField(
        default=True,
        verbose_name="Mode Test"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    class Meta:
        verbose_name = "Passerelle de paiement"
        verbose_name_plural = "Passerelles de paiement"
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==========================================================
#                 TRANSACTION DE PAIEMENT
# ==========================================================

class PaymentTransaction(BasePaymentModel):
    """
    Représente une transaction réelle envoyée
    vers une passerelle de paiement.

    Cette table permet de garder absolument
    toutes les opérations réalisées.
    """

    STATUS_CHOICES = [

        ("pending", "En attente"),

        ("processing", "Traitement"),

        ("success", "Succès"),

        ("failed", "Échec"),

        ("cancelled", "Annulé"),

        ("refunded", "Remboursé"),
    ]

    payment_reference = models.OneToOneField(
        PaymentReference,
        on_delete=models.PROTECT,
        related_name="transaction",
        verbose_name="Référence"
    )

    gateway = models.ForeignKey(
        PaymentGateway,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Passerelle"
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
        verbose_name="Méthode"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant"
    )

    currency = models.CharField(
        max_length=10,
        default="XOF",
        verbose_name="Devise"
    )

    phone_number = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Téléphone"
    )

    payer_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Nom du payeur"
    )

    payer_email = models.EmailField(
        blank=True,
        verbose_name="Email"
    )

    external_transaction_id = models.CharField(
        max_length=150,
        blank=True,
        unique=True,
        null=True,
        verbose_name="ID externe"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Statut"
    )

    payment_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date du paiement"
    )

    gateway_response = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Réponse API"
    )

    failure_reason = models.TextField(
        blank=True,
        verbose_name="Motif d'échec"
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name="Adresse IP"
    )

    user_agent = models.TextField(
        blank=True,
        verbose_name="Navigateur"
    )

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return self.payment_reference.reference
    # ==========================================================
#                    FACTURES
# ==========================================================

class Invoice(BasePaymentModel):
    """
    Facture générée avant ou après un paiement.

    Une facture peut concerner :

        • les frais de scolarité
        • les frais d'inscription
        • un document payant
        • un abonnement Premium
        • une formation
        • un concours

    Une facture peut être réglée en une ou plusieurs fois.
    """

    STATUS_CHOICES = [

        ("draft", "Brouillon"),

        ("pending", "En attente"),

        ("partial", "Partiellement payée"),

        ("paid", "Entièrement payée"),

        ("cancelled", "Annulée"),
    ]

    invoice_number = models.CharField(
        max_length=60,
        unique=True,
        verbose_name="Numéro de facture"
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Objet"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant total"
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Montant payé"
    )

    remaining_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Reste à payer"
    )

    issue_date = models.DateField(
        auto_now_add=True,
        verbose_name="Date d'émission"
    )

    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date limite"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Statut"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observations"
    )

    class Meta:
        verbose_name = "Facture"

        verbose_name_plural = "Factures"

        ordering = ["-issue_date"]

    def __str__(self):
        return self.invoice_number


# ==========================================================
#                       REÇUS
# ==========================================================

class Receipt(BasePaymentModel):
    """
    Reçu officiel délivré après validation
    d'un paiement.

    Chaque reçu possède :

        • un numéro unique

        • une référence unique

        • un code de vérification

        • un QR Code (généré plus tard)

    Un reçu ne pourra jamais être supprimé
    afin de garantir la traçabilité complète
    des paiements.
    """

    receipt_number = models.CharField(
        max_length=60,
        unique=True,
        verbose_name="Numéro du reçu"
    )

    payment = models.OneToOneField(
        PaymentTransaction,
        on_delete=models.PROTECT,
        related_name="receipt",
        verbose_name="Paiement"
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name="receipts",
        null=True,
        blank=True,
        verbose_name="Facture"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant"
    )

    issue_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'émission"
    )

    verification_code = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="Code de vérification"
    )

    qr_code = models.ImageField(
        upload_to="payments/qrcodes/",
        blank=True,
        null=True,
        verbose_name="QR Code"
    )

    pdf_receipt = models.FileField(
        upload_to="payments/receipts/",
        blank=True,
        null=True,
        verbose_name="Reçu PDF"
    )

    is_valid = models.BooleanField(
        default=True,
        verbose_name="Valide"
    )

    cancelled = models.BooleanField(
        default=False,
        verbose_name="Annulé"
    )

    cancellation_reason = models.TextField(
        blank=True,
        verbose_name="Motif d'annulation"
    )

    class Meta:
        verbose_name = "Reçu"

        verbose_name_plural = "Reçus"

        ordering = ["-issue_date"]

    def __str__(self):
        return self.receipt_number
    # ==========================================================
#                CAISSE DE L'ÉTABLISSEMENT
# ==========================================================

class SchoolCashRegister(BasePaymentModel):
    """
    Représente une caisse physique ou virtuelle
    d'un établissement scolaire.

    Une école peut posséder plusieurs caisses.

    Exemples :

        • Caisse principale
        • Caisse des inscriptions
        • Caisse comptabilité
        • Caisse examens
    """

    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nom de la caisse"
    )

    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Code"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Solde initial"
    )

    current_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Solde actuel"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    class Meta:
        verbose_name = "Caisse"
        verbose_name_plural = "Caisses"
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==========================================================
#              SESSION D'OUVERTURE DE CAISSE
# ==========================================================

class CashSession(BasePaymentModel):
    """
    Chaque journée de caisse correspond
    à une session.

    Une session possède :

        • une heure d'ouverture

        • une heure de fermeture

        • un montant d'ouverture

        • un montant de fermeture

    Ainsi chaque mouvement est parfaitement
    traçable.
    """

    STATUS_CHOICES = [

        ("open", "Ouverte"),

        ("closed", "Fermée"),
    ]

    cash_register = models.ForeignKey(
        SchoolCashRegister,
        on_delete=models.PROTECT,
        related_name="sessions",
        verbose_name="Caisse"
    )

    session_number = models.CharField(
        max_length=60,
        unique=True,
        verbose_name="Numéro"
    )

    opening_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ouverture"
    )

    closing_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fermeture"
    )

    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Montant d'ouverture"
    )

    closing_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Montant de fermeture"
    )

    total_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Total encaissé"
    )

    total_expense = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Total décaissement"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
        verbose_name="Statut"
    )

    observations = models.TextField(
        blank=True,
        verbose_name="Observations"
    )

    class Meta:
        verbose_name = "Session de caisse"
        verbose_name_plural = "Sessions de caisse"
        ordering = ["-opening_datetime"]

    def __str__(self):
        return self.session_number


# ==========================================================
#              PAIEMENT DES ÉLÈVES
# ==========================================================

class SchoolPayment(BasePaymentModel):
    """
    Paiement effectué par un élève.

    Ce modèle sera relié plus tard
    aux applications :

        • students

        • school

        • configuration

    Il constitue le cœur de la comptabilité
    scolaire.
    """

    STATUS_CHOICES = [

        ("pending", "En attente"),

        ("partial", "Paiement partiel"),

        ("paid", "Soldé"),

        ("cancelled", "Annulé"),
    ]

    payment_reference = models.OneToOneField(
        PaymentReference,
        on_delete=models.PROTECT,
        verbose_name="Référence"
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name="school_payments",
        verbose_name="Facture"
    )

    cash_session = models.ForeignKey(
        CashSession,
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name="Session"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant payé"
    )

    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="paid",
        verbose_name="Statut"
    )

    remarks = models.TextField(
        blank=True,
        verbose_name="Observations"
    )

    class Meta:
        verbose_name = "Paiement scolaire"
        verbose_name_plural = "Paiements scolaires"
        ordering = ["-payment_date"]

    def __str__(self):
        return self.payment_reference.reference
    # ==========================================================
#           PAIEMENT PAR TRANCHE
# ==========================================================

class PaymentInstallment(BasePaymentModel):
    """
    Permet de gérer les paiements effectués
    en plusieurs tranches.

    Exemple :

        Frais de scolarité : 150 000 FCFA

            • 50 000 FCFA
            • 40 000 FCFA
            • 60 000 FCFA

    Toutes les tranches sont conservées.
    """

    STATUS_CHOICES = [

        ("pending", "En attente"),

        ("paid", "Payée"),

        ("late", "En retard"),
    ]

    school_payment = models.ForeignKey(
        SchoolPayment,
        on_delete=models.CASCADE,
        related_name="installments",
        verbose_name="Paiement scolaire"
    )

    installment_number = models.PositiveIntegerField(
        verbose_name="Numéro de tranche"
    )

    expected_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant prévu"
    )

    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Montant payé"
    )

    due_date = models.DateField(
        verbose_name="Date limite"
    )

    payment_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de paiement"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Statut"
    )

    observations = models.TextField(
        blank=True,
        verbose_name="Observations"
    )

    class Meta:
        verbose_name = "Tranche de paiement"
        verbose_name_plural = "Tranches de paiement"
        ordering = [
            "school_payment",
            "installment_number"
        ]

    def __str__(self):
        return (
            f"{self.school_payment} "
            f"- Tranche {self.installment_number}"
        )


# ==========================================================
#                REMBOURSEMENTS
# ==========================================================

class Refund(BasePaymentModel):
    """
    Historique des remboursements.

    Aucun remboursement n'est supprimé.

    Toute opération reste enregistrée afin
    de garantir la traçabilité financière.
    """

    STATUS_CHOICES = [

        ("pending", "En attente"),

        ("approved", "Approuvé"),

        ("completed", "Effectué"),

        ("rejected", "Refusé"),
    ]

    transaction = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.PROTECT,
        related_name="refunds",
        verbose_name="Transaction"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant"
    )

    reason = models.TextField(
        verbose_name="Motif"
    )

    refund_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Statut"
    )

    class Meta:
        verbose_name = "Remboursement"
        verbose_name_plural = "Remboursements"
        ordering = ["-refund_date"]

    def __str__(self):
        return (
            f"Remboursement "
            f"{self.transaction.payment_reference.reference}"
        )
    # ==========================================================
#            VÉRIFICATION DES PAIEMENTS
# ==========================================================

class PaymentVerification(BasePaymentModel):
    """
    Vérification officielle d'un paiement.

    Cette table permet de savoir :

        • qui a vérifié le paiement

        • quand

        • le résultat

    Elle sera utilisée pour empêcher
    les faux reçus.
    """

    STATUS_CHOICES = [

        ("pending", "En attente"),

        ("verified", "Vérifié"),

        ("rejected", "Rejeté"),
    ]

    transaction = models.OneToOneField(
        PaymentTransaction,
        on_delete=models.PROTECT,
        related_name="verification",
        verbose_name="Transaction"
    )

    verification_code = models.CharField(
        max_length=80,
        unique=True,
        verbose_name="Code de vérification"
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de vérification"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Statut"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observations"
    )

    class Meta:
        verbose_name = "Vérification"
        verbose_name_plural = "Vérifications"

    def __str__(self):
        return self.verification_code


# ==========================================================
#            JOURNAL DE SÉCURITÉ
# ==========================================================

class PaymentAuditLog(BasePaymentModel):
    """
    Journal complet des opérations.

    Rien n'est supprimé.

    Chaque consultation, modification,
    validation ou annulation est enregistrée.
    """

    ACTION_CHOICES = [

        ("create", "Création"),

        ("update", "Modification"),

        ("delete", "Suppression"),

        ("payment", "Paiement"),

        ("refund", "Remboursement"),

        ("verification", "Vérification"),

        ("login", "Connexion"),

        ("logout", "Déconnexion"),
    ]

    transaction = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="Transaction"
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES,
        verbose_name="Action"
    )

    performed_by = models.CharField(
        max_length=200,
        verbose_name="Effectuée par"
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Adresse IP"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    class Meta:
        verbose_name = "Journal de sécurité"
        verbose_name_plural = "Journaux de sécurité"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} - {self.created_at}"


# ==========================================================
#            DÉTECTION DE FRAUDE
# ==========================================================

class FraudDetection(BasePaymentModel):
    """
    Détecte automatiquement les opérations
    suspectes.

    Exemples :

        • faux reçu

        • double paiement

        • tentative de fraude

        • modification suspecte

        • paiement inhabituel
    """

    LEVEL_CHOICES = [

        ("low", "Faible"),

        ("medium", "Moyen"),

        ("high", "Élevé"),

        ("critical", "Critique"),
    ]

    transaction = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.CASCADE,
        related_name="fraud_reports",
        verbose_name="Transaction"
    )

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default="low",
        verbose_name="Niveau"
    )

    detected_reason = models.TextField(
        verbose_name="Motif"
    )

    resolved = models.BooleanField(
        default=False,
        verbose_name="Résolu"
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de résolution"
    )

    class Meta:
        verbose_name = "Détection de fraude"
        verbose_name_plural = "Détections de fraude"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.level} - {self.transaction}"


# ==========================================================
#          VÉRIFICATION PAR QR CODE
# ==========================================================

class QRCodeVerification(BasePaymentModel):
    """
    Permet de vérifier un reçu simplement
    en scannant son QR Code.

    Même plusieurs années après,
    l'établissement pourra vérifier
    l'authenticité du reçu.
    """

    receipt = models.OneToOneField(
        Receipt,
        on_delete=models.CASCADE,
        related_name="qr_verification",
        verbose_name="Reçu"
    )

    qr_token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Jeton QR"
    )

    verification_url = models.URLField(
        blank=True,
        verbose_name="URL de vérification"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    class Meta:
        verbose_name = "QR Code sécurisé"
        verbose_name_plural = "QR Codes sécurisés"

    def __str__(self):
        return self.receipt.receipt_number
# ==========================================================
#         ABONNEMENTS PREMIUM DE LA PLATEFORME
# ==========================================================

class PlatformSubscription(BasePaymentModel):
    """
    Gère les abonnements Premium de la plateforme.

    Exemples :

        • Mensuel
        • Trimestriel
        • Semestriel
        • Annuel
    """

    DURATION_CHOICES = [

        ("1m", "1 mois"),

        ("3m", "3 mois"),

        ("6m", "6 mois"),

        ("12m", "12 mois"),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom"
    )

    duration = models.CharField(
        max_length=10,
        choices=DURATION_CHOICES,
        verbose_name="Durée"
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Prix"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    class Meta:
        verbose_name = "Abonnement Premium"
        verbose_name_plural = "Abonnements Premium"
        ordering = ["price"]

    def __str__(self):
        return self.name


# ==========================================================
#            ACHATS DE LA PLATEFORME
# ==========================================================

class PlatformPurchase(BasePaymentModel):
    """
    Historique des achats effectués
    sur la plateforme.

    Ce modèle sera relié plus tard aux
    applications Documents et Concours.
    """

    PURCHASE_TYPES = [

        ("document", "Document"),

        ("video", "Vidéo"),

        ("course", "Cours"),

        ("exercise", "Exercice"),

        ("exam", "Examen"),

        ("competition", "Concours"),

        ("subscription", "Abonnement"),

        ("other", "Autre"),
    ]

    payment_reference = models.OneToOneField(
        PaymentReference,
        on_delete=models.PROTECT,
        verbose_name="Référence"
    )

    purchase_type = models.CharField(
        max_length=30,
        choices=PURCHASE_TYPES,
        verbose_name="Type d'achat"
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Nom du produit"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant"
    )

    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Accès autorisé"
    )

    class Meta:
        verbose_name = "Achat de la plateforme"
        verbose_name_plural = "Achats de la plateforme"
        ordering = ["-payment_date"]

    def __str__(self):
        return self.title


# ==========================================================
#          LICENCES D'ACCÈS AUX CONTENUS
# ==========================================================

class AccessLicense(BasePaymentModel):
    """
    Une licence est créée après un achat.

    Elle permettra de vérifier
    qu'un utilisateur possède bien
    le droit d'accéder au contenu.
    """

    purchase = models.OneToOneField(
        PlatformPurchase,
        on_delete=models.CASCADE,
        related_name="license",
        verbose_name="Achat"
    )

    access_key = models.CharField(
        max_length=120,
        unique=True,
        verbose_name="Clé d'accès"
    )

    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Début"
    )

    expiration_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Expiration"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Licence active"
    )

    class Meta:
        verbose_name = "Licence d'accès"
        verbose_name_plural = "Licences d'accès"

    def __str__(self):
        return self.access_key


# ==========================================================
#             STATISTIQUES FINANCIÈRES
# ==========================================================

class PaymentStatistic(BasePaymentModel):
    """
    Stocke des statistiques financières.

    Elles permettront d'alimenter
    le tableau de bord administrateur.
    """

    label = models.CharField(
        max_length=100,
        verbose_name="Libellé"
    )

    value = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        verbose_name="Valeur"
    )

    statistic_date = models.DateField(
        default=timezone.now,
        verbose_name="Date"
    )

    class Meta:
        verbose_name = "Statistique financière"
        verbose_name_plural = "Statistiques financières"
        ordering = ["-statistic_date", "label"]

    def __str__(self):
        return self.label


# ==========================================================
#          WEBHOOKS DE PAIEMENT
# ==========================================================

class PaymentWebhook(BasePaymentModel):
    """
    Historique des notifications
    envoyées par les opérateurs.

    Chaque réponse provenant de MTN,
    Moov ou Stripe est conservée.
    """

    gateway = models.ForeignKey(
        PaymentGateway,
        on_delete=models.CASCADE,
        related_name="webhooks",
        verbose_name="Passerelle"
    )

    event = models.CharField(
        max_length=100,
        verbose_name="Evènement"
    )

    payload = models.JSONField(
        verbose_name="Réponse reçue"
    )

    processed = models.BooleanField(
        default=False,
        verbose_name="Traité"
    )

    class Meta:
        verbose_name = "Webhook"
        verbose_name_plural = "Webhooks"

    def __str__(self):
        return self.event


# ==========================================================
#         NOTIFICATIONS DE PAIEMENT
# ==========================================================

class PaymentNotification(BasePaymentModel):
    """
    Toutes les notifications envoyées
    aux utilisateurs.

    Exemples :

        • Paiement reçu

        • Paiement refusé

        • Paiement validé

        • Reçu disponible
    """

    CHANNELS = [

        ("sms", "SMS"),

        ("email", "Email"),

        ("push", "Notification"),

        ("whatsapp", "WhatsApp"),
    ]

    transaction = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Transaction"
    )

    channel = models.CharField(
        max_length=20,
        choices=CHANNELS,
        verbose_name="Canal"
    )

    recipient = models.CharField(
        max_length=255,
        verbose_name="Destinataire"
    )

    message = models.TextField(
        verbose_name="Message"
    )

    sent = models.BooleanField(
        default=False,
        verbose_name="Envoyé"
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date d'envoi"
    )

    class Meta:
        verbose_name = "Notification de paiement"
        verbose_name_plural = "Notifications de paiement"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.channel} - {self.recipient}"


# ==========================================================
#              GRAND LIVRE COMPTABLE
# ==========================================================

class LedgerEntry(BasePaymentModel):
    """
    Grand livre comptable.

    Chaque paiement validé génère automatiquement
    une écriture comptable.

    Rien n'est supprimé.
    """

    ENTRY_TYPES = [

        ("credit", "Crédit"),

        ("debit", "Débit"),
    ]

    transaction = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.PROTECT,
        related_name="ledger_entries",
        verbose_name="Transaction"
    )

    entry_type = models.CharField(
        max_length=20,
        choices=ENTRY_TYPES,
        verbose_name="Type"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    entry_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date"
    )

    class Meta:
        verbose_name = "Écriture comptable"
        verbose_name_plural = "Grand livre comptable"
        ordering = ["-entry_date"]

    def __str__(self):
        return f"{self.entry_type} - {self.amount}"