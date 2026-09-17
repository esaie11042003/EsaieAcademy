from django import forms
from .models import Classe
from teachers.models import Teacher


class ClasseForm(forms.ModelForm):

    class Meta:
        model = Classe
        fields = ["nom", "matieres", "professeur_principal", "couleur_bulletin", "style_bordure"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : 6ème A, Terminale D..."}),
            "matieres": forms.CheckboxSelectMultiple(),
            "professeur_principal": forms.Select(attrs={"class": "form-select"}),
            "couleur_bulletin": forms.Select(attrs={"class": "form-select"}),
            "style_bordure": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop("school", None)
        super().__init__(*args, **kwargs)
        self.fields["professeur_principal"].required = False

        queryset = Teacher.objects.all()
        if school is not None:
            filtre = Teacher.objects.filter(school_access__school=school).distinct()
            if filtre.exists():
                queryset = filtre
        self.fields["professeur_principal"].queryset = queryset