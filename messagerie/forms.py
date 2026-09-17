from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["body", "fichier"]
        widgets = {
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Écrire un message..."}),
            "fichier": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class RechercheUtilisateurForm(forms.Form):
    identifiant = forms.CharField(
        label="Nom d'utilisateur ou email de la personne",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : marie.dupont"})
    )