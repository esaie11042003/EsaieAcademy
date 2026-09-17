from django import forms
from .models import Assignment
from teachers.models import Teacher
from classes.models import Classe


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ["teacher", "classe", "subject", "school_year", "coefficient", "active"]
        widgets = {
            "teacher": forms.Select(attrs={"class": "form-select"}),
            "classe": forms.Select(attrs={"class": "form-select"}),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "school_year": forms.Select(attrs={"class": "form-select"}),
            "coefficient": forms.NumberInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, school=None, **kwargs):
        super().__init__(*args, **kwargs)
        if school:
            self.fields["teacher"].queryset = Teacher.objects.filter(school_access__school=school).distinct()
            self.fields["classe"].queryset = Classe.objects.filter(school=school)