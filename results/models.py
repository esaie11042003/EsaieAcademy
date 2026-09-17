from django.db import models

from students.models import Eleve
from assignments.models import Assignment
from school.models import Period


class SubjectResult(models.Model):
    """
    Résultat d'un élève dans une matière
    pour une période donnée.
    """

    eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="subject_results"
    )

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="subject_results"
    )

    period = models.ForeignKey(
        Period,
        on_delete=models.CASCADE,
        related_name="subject_results"
    )

    moyenne_interrogations = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    devoir_1 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    devoir_2 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    moyenne = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    coefficient = models.PositiveIntegerField(
        default=1
    )

    points = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0
    )

    rang = models.PositiveIntegerField(
        default=0
    )

    appreciation = models.CharField(
        max_length=100,
        blank=True
    )

    observation = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = "Résultat par matière"
        verbose_name_plural = "Résultats par matière"
        ordering = [
            "assignment",
            "rang",
        ]
        unique_together = (
            "eleve",
            "assignment",
            "period",
        )

    def __str__(self):
        return (
            f"{self.eleve} - "
            f"{self.assignment.subject}"
        )


class StudentResult(models.Model):
    """
    Résultat général d'un élève
    pour une période.
    """

    DECISION_CHOICES = (
        ("ADMIS", "Admis"),
        ("REDOUBLE", "Redouble"),
        ("EXCLU", "Exclu"),
    )

    eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="student_results"
    )

    period = models.ForeignKey(
        Period,
        on_delete=models.CASCADE,
        related_name="student_results"
    )

    total_points = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    total_coefficients = models.PositiveIntegerField(
        default=0
    )

    moyenne_generale = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    # ========================================================
    # NOUVEAU : moyennes par grand groupe de matières
    # ========================================================

    moyenne_scientifique = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Moyenne matières scientifiques"
    )

    moyenne_litteraire = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Moyenne matières littéraires"
    )

    rang = models.PositiveIntegerField(
        default=0
    )

    mention = models.CharField(
        max_length=50,
        blank=True
    )

    decision = models.CharField(
        max_length=20,
        choices=DECISION_CHOICES,
        blank=True
    )

    appreciation = models.TextField(
        blank=True
    )

    # ========================================================
    # NOUVEAU : conduite, récompenses/sanctions, assiduité
    # Ces champs sont saisis MANUELLEMENT par le staff — ils ne
    # sont jamais écrasés par le recalcul automatique des notes.
    # ========================================================

    conduite = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Conduite"
    )

    felicitations = models.BooleanField(default=False, verbose_name="Félicitations")
    encouragements = models.BooleanField(default=False, verbose_name="Encouragements")
    tableau_honneur = models.BooleanField(default=False, verbose_name="Tableau d'honneur")

    avertissement = models.BooleanField(default=False, verbose_name="Avertissement")
    blame = models.BooleanField(default=False, verbose_name="Blâme")
    travail_acceptable = models.BooleanField(default=False, verbose_name="Travail acceptable")

    heures_absence = models.PositiveIntegerField(
        default=0,
        verbose_name="Heures d'absence"
    )

    generated_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Résultat général"
        verbose_name_plural = "Résultats généraux"
        ordering = [
            "period",
            "rang",
        ]
        unique_together = (
            "eleve",
            "period",
        )

    def __str__(self):
        return f"{self.eleve} - {self.period}"