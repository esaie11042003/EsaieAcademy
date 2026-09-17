from django.db import models

# Create your models here.
class PlatformBranding(models.Model):
    """
    Réglages graphiques globaux de la plateforme, communs à tous
    les établissements. Un seul enregistrement doit exister.
    """

    logo_devise_benin = models.ImageField(
        upload_to="platform_admin/branding/",
        blank=True,
        null=True,
        verbose_name="Logo de la devise du Bénin (Fraternité-Justice-Travail)"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Réglages graphiques de la plateforme"
        verbose_name_plural = "Réglages graphiques de la plateforme"

    def __str__(self):
        return "Réglages graphiques de la plateforme"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj