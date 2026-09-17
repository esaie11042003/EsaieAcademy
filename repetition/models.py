import random
import string

from django.db import models
from django.conf import settings


class DemandeMaitreEtude(models.Model):

    STATUT_CHOICES = (
        ("nouvelle", "Nouvelle"),
        ("en_discussion", "En discussion"),
        ("rdv_planifie", "Rendez-vous planifié"),
        ("cloturee", "Clôturée"),
    )

    demandeur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="demandes_maitre_etude"
    )

    code_suivi = models.CharField(
        max_length=8, unique=True, blank=True,
        verbose_name="Code de suivi"
    )

    nom_contact = models.CharField(max_length=150, verbose_name="Nom complet")
    telephone_contact = models.CharField(max_length=30, verbose_name="Téléphone")
    email_contact = models.EmailField(blank=True, verbose_name="Email (optionnel)")

    matiere = models.CharField(max_length=100, verbose_name="Matière")
    classe_enfant = models.CharField(max_length=50, verbose_name="Classe de l'enfant")
    zone = models.CharField(max_length=150, verbose_name="Zone / Quartier")
    college_enfant = models.CharField(max_length=200, blank=True, verbose_name="Collège / École de l'enfant")
    niveau_professeur_voulu = models.CharField(max_length=100, blank=True, verbose_name="Niveau du professeur souhaité")
    message = models.TextField(blank=True, verbose_name="Informations complémentaires")

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="nouvelle")
    traite_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="demandes_traitees"
    )

    rdv_date = models.DateTimeField(null=True, blank=True, verbose_name="Date du rendez-vous")
    rdv_lieu = models.CharField(max_length=200, blank=True, verbose_name="Lieu / Moyen du rendez-vous")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Demande de maître d'étude"
        verbose_name_plural = "Demandes de maître d'étude"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.code_suivi:
            caracteres = string.ascii_uppercase + string.digits
            while True:
                code = "".join(random.choices(caracteres, k=6))
                if not DemandeMaitreEtude.objects.filter(code_suivi=code).exists():
                    self.code_suivi = code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom_contact} — {self.matiere} ({self.classe_enfant})"


class MessageDemande(models.Model):

    demande = models.ForeignKey(
        DemandeMaitreEtude,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="messages_demande_maitre_etude"
    )
    # Distingue un message écrit par l'admin de celui écrit par le demandeur
    # (le demandeur peut être anonyme, donc auteur peut être vide).
    is_admin = models.BooleanField(default=False)
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message sur {self.demande}"