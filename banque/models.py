from django.db import models
from django.conf import settings
from classes.models import Classe


class EpreuveClasse(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="epreuves_banque")
    titre = models.CharField(max_length=200)
    annee = models.PositiveIntegerField()
    fichier_sujet = models.FileField(upload_to="banque/epreuves/sujets/")
    fichier_corrige = models.FileField(upload_to="banque/epreuves/corriges/", blank=True, null=True)
    ajoute_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_payant = models.BooleanField(default=False, verbose_name="Payant")
    prix = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Prix (FCFA)")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.classe.nom} — {self.titre} ({self.annee})"

    class Meta:
        ordering = ["-annee", "classe"]


class DocumentClasse(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="documents_banque")
    titre = models.CharField(max_length=200)
    annee = models.PositiveIntegerField()
    fichier = models.FileField(upload_to="banque/documents/")
    ajoute_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_payant = models.BooleanField(default=False, verbose_name="Payant")
    prix = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Prix (FCFA)")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.classe.nom} — {self.titre} ({self.annee})"

    class Meta:
        ordering = ["-annee", "classe"]