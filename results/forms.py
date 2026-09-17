from django import forms
from .models import StudentResult


class ConduiteForm(forms.ModelForm):

    class Meta:
        model = StudentResult
        fields = [
            "conduite",
            "felicitations",
            "encouragements",
            "tableau_honneur",
            "avertissement",
            "blame",
            "travail_acceptable",
            "heures_absence",
        ]
        widgets = {
            "conduite": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : Excellent, Bien, Passable...",
            }),
            "heures_absence": forms.NumberInput(attrs={"class": "form-control"}),
        }