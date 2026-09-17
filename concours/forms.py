from django import forms
from .models import Concours, EpreuveConcours


class ConcoursForm(forms.ModelForm):
    class Meta:
        model = Concours
        fields = ["nom", "description"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : Police, Douane, ENA..."}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class EpreuveConcoursForm(forms.ModelForm):
    class Meta:
        model = EpreuveConcours
        fields = ["concours", "titre", "annee", "fichier_sujet", "fichier_corrige", "is_payant", "prix"]
        widgets = {
            "concours": forms.Select(attrs={"class": "form-select"}),
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "annee": forms.NumberInput(attrs={"class": "form-control"}),
            "fichier_sujet": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "fichier_corrige": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_payant": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prix": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Laisser vide si gratuit"}),
        }