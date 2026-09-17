from django import forms
from .models import ReceivingAccount, Purchase


class ReceivingAccountForm(forms.ModelForm):
    class Meta:
        model = ReceivingAccount
        fields = ["numero", "actif", "note"]
        widgets = {
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "actif": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "note": forms.TextInput(attrs={"class": "form-control"}),
        }


class AchatForm(forms.Form):
    operateur = forms.ChoiceField(
        choices=ReceivingAccount.OPERATEUR_CHOICES,
        widget=forms.RadioSelect
    )
    reference_paiement = forms.CharField(
        label="Référence / ID de la transaction (reçu par SMS après le paiement)",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )