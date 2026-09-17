from django.db import models


class SchoolYear(models.Model):
    """
    Représente une année scolaire.
    Exemple : 2025-2026
    """

    nom = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Nom"
    )

    date_debut = models.DateField(
        verbose_name="Date de début"
    )

    date_fin = models.DateField(
        verbose_name="Date de fin"
    )

    active = models.BooleanField(
        default=False,
        verbose_name="Année active"
    )

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Année scolaire"
        verbose_name_plural = "Années scolaires"
        ordering = ["-date_debut"]


class Period(models.Model):
    """
    Représente une période scolaire.
    (Trimestre ou Semestre)
    """

    PERIOD_CHOICES = (
        ("T1", "1er Trimestre"),
        ("T2", "2ème Trimestre"),
        ("T3", "3ème Trimestre"),
        ("S1", "1er Semestre"),
        ("S2", "2ème Semestre"),
    )

    school_year = models.ForeignKey(
        SchoolYear,
        on_delete=models.CASCADE,
        related_name="periods",
        verbose_name="Année scolaire"
    )

    name = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        verbose_name="Période"
    )

    start_date = models.DateField(
        verbose_name="Date de début"
    )

    end_date = models.DateField(
        verbose_name="Date de fin"
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name="Période active"
    )

    def __str__(self):
        return f"{self.get_name_display()} ({self.school_year})"

    class Meta:
        verbose_name = "Période"
        verbose_name_plural = "Périodes"
        ordering = ["school_year", "start_date"]