from django.db import models
from django.core.exceptions import ValidationError

from assignments.models import Assignment
from students.models import Eleve
from school.models import Period


class Evaluation(models.Model):

    TYPE_CHOICES = (
        ("INTERROGATION", "Interrogation"),
        ("DEVOIR", "Devoir"),
    )

    STATUT_CHOICES = (
        ("BROUILLON", "Brouillon"),
        ("PUBLIE", "Publié"),
        ("VERROUILLE", "Verrouillé"),
    )

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="evaluations"
    )

    period = models.ForeignKey(
        Period,
        on_delete=models.CASCADE,
        related_name="evaluations"
    )

    evaluation_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )

    numero = models.PositiveSmallIntegerField()

    date = models.DateField()

    note_sur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=20
    )

    publier = models.BooleanField(
        default=False
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="BROUILLON"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Évaluation"
        verbose_name_plural = "Évaluations"
        ordering = [
            "assignment",
            "period",
            "evaluation_type",
            "numero",
        ]
        unique_together = (
            "assignment",
            "period",
            "evaluation_type",
            "numero",
        )

    def clean(self):

        # Vérifie que l'année scolaire correspond
        if self.assignment.school_year != self.period.school_year:
            raise ValidationError(
                "L'affectation et la période doivent appartenir à la même année scolaire."
            )

        # Maximum de 4 interrogations
        if self.evaluation_type == "INTERROGATION" and self.numero > 4:
            raise ValidationError(
                "Une matière ne peut pas avoir plus de 4 interrogations."
            )

        # Maximum de 2 devoirs
        if self.evaluation_type == "DEVOIR" and self.numero > 2:
            raise ValidationError(
                "Une matière ne peut pas avoir plus de 2 devoirs."
            )

        # Numéro minimum
        if self.numero < 1:
            raise ValidationError(
                "Le numéro doit être supérieur ou égal à 1."
            )

    def __str__(self):
        return (
            f"{self.get_evaluation_type_display()} "
            f"{self.numero} - "
            f"{self.assignment}"
        )


class Note(models.Model):

    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    note = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    absent = models.BooleanField(
        default=False
    )

    observation = models.CharField(
        max_length=255,
        blank=True
    )
    modified_by = models.ForeignKey(
        "accounts.CustomUser",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="notes_modifiees"
    )

    modification_reason = models.TextField(
        blank=True,
        verbose_name="Raison de la modification"
    )

    is_deleted = models.BooleanField(
        default=False
    )

    deleted_by = models.ForeignKey(
        "accounts.CustomUser",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="notes_supprimees"
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    deletion_reason = models.TextField(
        blank=True,
        verbose_name="Raison de la suppression"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = [
            "eleve",
        ]
        unique_together = (
            "evaluation",
            "eleve",
        )

    def __str__(self):
        return (
            f"{self.eleve} - "
            f"{self.evaluation} : "
            f"{self.note}"
        )