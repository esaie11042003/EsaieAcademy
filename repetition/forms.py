from django import forms
from .models import DemandeMaitreEtude, MessageDemande


class DemandeMaitreEtudeForm(forms.ModelForm):

    class Meta:
        model = DemandeMaitreEtude
        fields = [
            "nom_contact", "telephone_contact", "email_contact",
            "matiere", "classe_enfant", "zone", "college_enfant",
            "niveau_professeur_voulu", "message",
        ]
        widgets = {
            "nom_contact": forms.TextInput(attrs={"class": "form-control"}),
            "telephone_contact": forms.TextInput(attrs={"class": "form-control"}),
            "email_contact": forms.EmailInput(attrs={"class": "form-control"}),
            "matiere": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : Mathématiques"}),
            "classe_enfant": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : 5ème"}),
            "zone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : Godomey, Calavi..."}),
            "college_enfant": forms.TextInput(attrs={"class": "form-control"}),
            "niveau_professeur_voulu": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : Étudiant, Licence, Professeur titulaire (optionnel)"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class MessageDemandeForm(forms.ModelForm):

    class Meta:
        model = MessageDemande
        fields = ["contenu"]
        widgets = {
            "contenu": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Écrire une réponse..."}),
        }


class RdvForm(forms.ModelForm):

    class Meta:
        model = DemandeMaitreEtude
        fields = ["rdv_date", "rdv_lieu", "statut"]
        widgets = {
            "rdv_date": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "rdv_lieu": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : Appel téléphonique, au domicile, à l'école..."}),
            "statut": forms.Select(attrs={"class": "form-select"}),
        }


class SuiviForm(forms.Form):
    """Formulaire public pour retrouver une demande sans être connecté."""
    telephone = forms.CharField(
        label="Téléphone utilisé lors de la demande",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    code_suivi = forms.CharField(
        label="Code de suivi",
        max_length=8,
        widget=forms.TextInput(attrs={"class": "form-control text-uppercase", "placeholder": "Ex : 7F3K9A"})
    )

    def clean_code_suivi(self):
        return self.cleaned_data["code_suivi"].strip().upper()