from django import forms
from .models import Examen, EpreuveExamen


class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ["nom", "description"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : BAC, BEPC, CEP..."}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class EpreuveExamenForm(forms.ModelForm):
    class Meta:
        model = EpreuveExamen
        fields = ["examen", "titre", "annee", "fichier_sujet", "fichier_corrige", "is_payant", "prix"]
        widgets = {
            "examen": forms.Select(attrs={"class": "form-select"}),
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "annee": forms.NumberInput(attrs={"class": "form-control"}),
            "fichier_sujet": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "fichier_corrige": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_payant": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prix": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Laisser vide si gratuit"}),
        }