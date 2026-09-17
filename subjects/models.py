from django.db import models


class Subject(models.Model):

    CATEGORIE_CHOICES = (
        ("scientifique", "Scientifique"),
        ("litteraire", "Littéraire"),
    )

    nom = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    categorie = models.CharField(
        max_length=20,
        choices=CATEGORIE_CHOICES,
        blank=True,
        verbose_name="Catégorie"
    )

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ["nom"]