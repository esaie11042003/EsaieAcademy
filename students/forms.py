from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from classes.models import Classe
from .models import Eleve


class RechercheEleveForm(forms.Form):
    identifiant = forms.CharField(
        label="Nom d'utilisateur ou email de l'élève",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : marie.eleve"})
    )
    matricule = forms.CharField(
        label="Matricule",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : ESA-2026-014"})
    )
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.none(),
        label="Classe",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def __init__(self, *args, school=None, **kwargs):
        super().__init__(*args, **kwargs)
        if school:
            self.fields["classe"].queryset = Classe.objects.filter(school=school)


class InscriptionEleveForm(UserCreationForm):

    matricule = forms.CharField(
        label="Matricule",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    sexe = forms.ChoiceField(
        choices=Eleve.SEXE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    date_naissance = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.none(),
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
        self.fields["email"].required = False
        self.fields["phone"].required = False
        if school:
            self.fields["classe"].queryset = Classe.objects.filter(school=school)

class EleveEditForm(forms.ModelForm):

    class Meta:
        model = Eleve
        fields = ["nom", "prenom", "sexe", "date_naissance", "statut", "npi", "matricule", "classe"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "sexe": forms.Select(attrs={"class": "form-select"}),
            "date_naissance": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "statut": forms.Select(attrs={"class": "form-select"}),
            "npi": forms.TextInput(attrs={"class": "form-control"}),
            "matricule": forms.TextInput(attrs={"class": "form-control"}),
            "classe": forms.Select(attrs={"class": "form-select"}),
        }


class CodeParentForm(forms.Form):
    code = forms.CharField(
        label="Code fourni par l'établissement",
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control text-uppercase",
            "placeholder": "Ex : 7F3K9A2B",
        })
    )

    def clean_code(self):
        return self.cleaned_data["code"].strip().upper()         