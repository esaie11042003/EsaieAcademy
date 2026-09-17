from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from .models import SchoolProfile, StaffRole


class SchoolProfileForm(forms.ModelForm):

    class Meta:
        model = SchoolProfile
        fields = [
            "nom",
            "sigle",
            "type_etablissement",
            "adresse",
            "ville",
            "telephone",
            "email",
        ]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : Collège Catholique Saint Michel"}),
            "sigle": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : CSM"}),
            "type_etablissement": forms.Select(attrs={"class": "form-select"}),
            "adresse": forms.TextInput(attrs={"class": "form-control"}),
            "ville": forms.TextInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class SchoolProfileEditForm(forms.ModelForm):
    """
    Formulaire complet de modification de l'établissement,
    utilisé après la création : coordonnées, logo, cachet.
    """

    class Meta:
        model = SchoolProfile
        fields = [
            "nom",
            "sigle",
            "type_etablissement",
            "devise",
            "logo",
            "cachet",
            "adresse",
            "ville",
            "telephone",
            "telephone_secondaire",
            "whatsapp",
            "email",
            "site_web",
            "description",
        ]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "sigle": forms.TextInput(attrs={"class": "form-control"}),
            "type_etablissement": forms.Select(attrs={"class": "form-select"}),
            "devise": forms.TextInput(attrs={"class": "form-control", "placeholder": "Devise de l'établissement (optionnel)"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "cachet": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "adresse": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : BP 09 Godomey"}),
            "ville": forms.TextInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "telephone_secondaire": forms.TextInput(attrs={"class": "form-control"}),
            "whatsapp": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "site_web": forms.URLInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class RechercheStaffForm(forms.Form):
    identifiant = forms.CharField(
        label="Nom d'utilisateur ou email",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : marie.secretaire"})
    )
    fonction = forms.CharField(
        label="Fonction",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : Secrétaire, Censeur..."})
    )


class InscriptionStaffForm(UserCreationForm):

    fonction = forms.CharField(
        label="Fonction",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : Secrétaire, Censeur..."})
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "fonction",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})