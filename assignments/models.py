from django.db import models
from teachers.models import Teacher
from classes.models import Classe
from subjects.models import Subject
from school.models import SchoolYear


class Assignment(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )

    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    school_year = models.ForeignKey(
        SchoolYear,
        on_delete=models.CASCADE
    )

    coefficient = models.PositiveIntegerField(
        default=1
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.teacher} - {self.subject} - {self.classe}"