from django import forms
from .models import EpreuveClasse, DocumentClasse


class EpreuveClasseForm(forms.ModelForm):
    class Meta:
        model = EpreuveClasse
        fields = ["classe", "titre", "annee", "fichier_sujet", "fichier_corrige", "is_payant", "prix"]
        widgets = {
            "classe": forms.Select(attrs={"class": "form-select"}),
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "annee": forms.NumberInput(attrs={"class": "form-control"}),
            "fichier_sujet": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "fichier_corrige": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_payant": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prix": forms.NumberInput(attrs={"class": "form-control"}),
        }


class DocumentClasseForm(forms.ModelForm):
    class Meta:
        model = DocumentClasse
        fields = ["classe", "titre", "annee", "fichier", "is_payant", "prix"]
        widgets = {
            "classe": forms.Select(attrs={"class": "form-select"}),
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "annee": forms.NumberInput(attrs={"class": "form-control"}),
            "fichier": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_payant": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prix": forms.NumberInput(attrs={"class": "form-control"}),
        }