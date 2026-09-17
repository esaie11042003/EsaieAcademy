from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from subjects.models import Subject
from classes.models import Classe


class RechercheEnseignantForm(forms.Form):
    identifiant = forms.CharField(
        label="Nom d'utilisateur ou email de l'enseignant",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : jean.kokou ou jean@email.com"})
    )


class InscriptionEnseignantForm(UserCreationForm):

    matieres = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        label="Matières enseignées"
    )

    classes = forms.ModelMultipleChoiceField(
        queryset=Classe.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        label="Classes"
    )

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

    def __init__(self, *args, school=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})
        if school:
            self.fields["classes"].queryset = Classe.objects.filter(school=school)


class PinForm(forms.Form):
    pin_code = forms.CharField(
        label="Code PIN de l'établissement",
        max_length=6,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "••••"})
    )


class ProfilEnseignantForm(forms.Form):
    phone = forms.CharField(
        label="Téléphone",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    adresse = forms.CharField(
        label="Adresse",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    bio = forms.CharField(
        label="Présentation (optionnel)",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3})
    )