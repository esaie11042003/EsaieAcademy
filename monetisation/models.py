from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class ReceivingAccount(models.Model):

    OPERATEUR_CHOICES = (
        ("MTN", "MTN Mobile Money"),
        ("CELTIS", "Celtiis Cash"),
        ("MOOV", "Moov Money"),
    )

    operateur = models.CharField(max_length=10, choices=OPERATEUR_CHOICES, unique=True)
    numero = models.CharField(max_length=20, verbose_name="Numéro de réception")
    actif = models.BooleanField(default=True)
    note = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_operateur_display()} — {self.numero}"


class Purchase(models.Model):

    STATUT_CHOICES = (
        ("EN_ATTENTE", "En attente de validation"),
        ("VALIDE", "Validé"),
        ("REJETE", "Rejeté"),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    resource = GenericForeignKey("content_type", "object_id")

    acheteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="achats"
    )

    operateur = models.CharField(max_length=10, choices=ReceivingAccount.OPERATEUR_CHOICES)
    numero_reception = models.CharField(max_length=20)
    montant = models.DecimalField(max_digits=10, decimal_places=0)
    reference_paiement = models.CharField(
        max_length=100,
        verbose_name="Référence / ID de la transaction reçue par SMS"
    )

    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default="EN_ATTENTE")

    created_at = models.DateTimeField(auto_now_add=True)
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="achats_valides"
    )
    validated_at = models.DateTimeField(null=True, blank=True)
    note_admin = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.acheteur} — {self.resource} — {self.montant} FCFA"