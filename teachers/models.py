from django.db import models
from accounts.models import CustomUser
from subjects.models import Subject
from classes.models import Classe
from configuration.models import SchoolProfile


class Teacher(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    adresse = models.CharField(
        max_length=255,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    matieres = models.ManyToManyField(
        Subject,
        related_name="teachers",
        blank=True
    )

    classes = models.ManyToManyField(
        Classe,
        related_name="teachers",
        blank=True
    )

    disponible = models.BooleanField(
        default=True
    )

    date_inscription = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class TeacherSchoolAccess(models.Model):
    """
    Relie un enseignant à un établissement, avec un code PIN
    propre à cet établissement (donné par son administration)
    pour protéger l'accès aux classes/notes de cette école.
    """

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="school_access"
    )

    school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="teacher_access"
    )

    pin_code = models.CharField(
        max_length=6,
        verbose_name="Code PIN"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("teacher", "school")

    def __str__(self):
        return f"{self.teacher} — {self.school}"