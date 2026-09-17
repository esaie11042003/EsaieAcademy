from django import forms
from .models import Forum, ForumMessage
from classes.models import Classe
from configuration.models import SchoolProfile


class ForumForm(forms.ModelForm):

    class Meta:
        model = Forum
        fields = ["nom", "description", "actif"]
        widgets = {
            "nom": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : Élèves de 3ème, Enseignants CEG1 Godomey...",
            }),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "actif": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ForumMessageForm(forms.ModelForm):

    class Meta:
        model = ForumMessage
        fields = ["contenu", "fichier"]
        widgets = {
            "contenu": forms.Textarea(attrs={
                "class": "form-control", "rows": 2, "placeholder": "Écrire un message...",
            }),
            "fichier": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class AjoutMembreForm(forms.Form):
    identifiant = forms.CharField(
        label="Nom d'utilisateur ou email",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : marie.dupont"})
    )


ROLE_CHOICES_BULK = (
    ("", "-- Choisir un critère --"),
    ("student", "Tous les élèves"),
    ("teacher", "Tous les enseignants"),
    ("staff", "Tout le personnel administratif"),
    ("parent", "Tous les parents"),
    ("admin", "Tous les co-administrateurs"),
)


class AjoutParCritereForm(forms.Form):
    role = forms.ChoiceField(
        label="Ajouter en masse",
        choices=ROLE_CHOICES_BULK,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    classe = forms.ModelChoiceField(
        label="Limiter à une classe (élèves uniquement)",
        queryset=Classe.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    ecole = forms.ModelChoiceField(
        label="Limiter à un établissement (enseignants / personnel)",
        queryset=SchoolProfile.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )