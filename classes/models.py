from django.db import models
from configuration.models import SchoolProfile


class Classe(models.Model):

    COULEUR_CHOICES = (
        ("bleu", "Bleu"),
        ("orange", "Orange"),
        ("rouge", "Rouge"),
        ("vert", "Vert"),
        ("violet", "Violet"),
        ("noir", "Noir"),
    )

    BORDURE_CHOICES = (
        (1, "Simple"),
        (2, "Double trait"),
        (3, "En creux (groove)"),
        (4, "En relief (ridge)"),
    )

    school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="classes",
        null=True,
        blank=True,
        verbose_name="Établissement"
    )

    nom = models.CharField(max_length=58)

    matieres = models.ManyToManyField(
        "subjects.Subject",
        blank=True
    )

    professeur_principal = models.ForeignKey(
        "teachers.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="classes_principales",
        verbose_name="Professeur Principal"
    )

    couleur_bulletin = models.CharField(
        max_length=20,
        choices=COULEUR_CHOICES,
        default="bleu",
        verbose_name="Couleur du bulletin"
    )

    style_bordure = models.PositiveSmallIntegerField(
        choices=BORDURE_CHOICES,
        default=1,
        verbose_name="Style de bordure du bulletin"
    )

    def __str__(self):
        if self.school:
            return f"{self.nom} — {self.school.nom}"
        return self.nom

    class Meta:
        unique_together = ("school", "nom")