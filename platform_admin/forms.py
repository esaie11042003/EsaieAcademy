from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser


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
        from django import forms
from .models import PlatformBranding


class PlatformBrandingForm(forms.ModelForm):

    class Meta:
        model = PlatformBranding
        fields = ["logo_devise_benin"]
        widgets = {
            "logo_devise_benin": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }