from django.db import models
from django.conf import settings


class Concours(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Concours"
        verbose_name_plural = "Concours"
        ordering = ["nom"]


class EpreuveConcours(models.Model):
    concours = models.ForeignKey(
        Concours, on_delete=models.CASCADE, related_name="epreuves"
    )
    titre = models.CharField(max_length=200)
    annee = models.PositiveIntegerField()
    fichier_sujet = models.FileField(upload_to="concours/sujets/")
    fichier_corrige = models.FileField(
        upload_to="concours/corriges/", blank=True, null=True
    )
    ajoute_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    is_payant = models.BooleanField(default=False, verbose_name="Payant")
    prix = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Prix (FCFA)")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.concours.nom} — {self.titre} ({self.annee})"

    class Meta:
        ordering = ["-annee", "concours"]