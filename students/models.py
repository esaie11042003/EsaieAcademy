import random
import string

from django.db import models
from django.conf import settings
from classes.models import Classe


class Eleve(models.Model):

    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    STATUT_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('ancien', 'Ancien'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="eleve",
        null=True,
        blank=True,
        verbose_name="Compte utilisateur"
    )

    matricule = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Matricule"
    )

    npi = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="NPI"
    )

    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default="nouveau",
        verbose_name="Statut"
    )

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    date_naissance = models.DateField()

    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='eleves'
    )

    parents = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="enfants",
        blank=True,
        verbose_name="Parents"
    )

    code_parent = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Code de liaison parent"
    )

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def generer_code_parent(self):
        """Génère un code unique (ex: 7F3K9A2B) et le sauvegarde."""
        caracteres = string.ascii_uppercase + string.digits
        while True:
            code = "".join(random.choices(caracteres, k=8))
            if not Eleve.objects.filter(code_parent=code).exists():
                self.code_parent = code
                self.save(update_fields=["code_parent"])
                return code

    class Meta:
        ordering = [
            "classe",
            "nom",
            "prenom",
        ]