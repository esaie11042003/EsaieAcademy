from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class InscriptionForm(UserCreationForm):

    ROLE_CHOICES_PUBLIC = (
        ("student", "Élève"),
        ("teacher", "Enseignant"),
        ("parent", "Parent"),
        ("staff", "Personnel administratif"),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES_PUBLIC,
        label="Je suis...",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "niveau_etude",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "niveau_etude": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class CompleterProfilForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ["phone", "adresse", "sexe", "date_naissance"]
        widgets = {
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "adresse": forms.TextInput(attrs={"class": "form-control"}),
            "sexe": forms.Select(attrs={"class": "form-select"}),
            "date_naissance": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].required = False
        self.fields["adresse"].required = False
        self.fields["date_naissance"].required = False


class RechercheAdminForm(forms.Form):
    identifiant = forms.CharField(
        label="Nom d'utilisateur ou email",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : marie.admin"})
    )


class InscriptionAdminForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
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