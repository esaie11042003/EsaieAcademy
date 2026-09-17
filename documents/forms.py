from django import forms
from .models import Document, DocumentCategory, DocumentType


class DocumentForm(forms.ModelForm):
    fichier = forms.FileField(
        label="Fichier (sujet)",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    fichier_corrige = forms.FileField(
        label="Corrigé (optionnel — vous pourrez l'ajouter ou le remplacer plus tard)",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Document
        fields = [
            "title", "category", "document_type", "subject", "classe",
            "level", "access_type", "prix", "short_description", "description",
        ]
  
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "document_type": forms.Select(attrs={"class": "form-select"}),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "classe": forms.Select(attrs={"class": "form-select"}),
            "level": forms.Select(attrs={"class": "form-select"}),
            "access_type": forms.Select(attrs={"class": "form-select"}),
            "short_description": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
                        "prix": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Laisser vide si gratuit"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].required = False
        self.fields["classe"].required = False
        self.fields["short_description"].required = False
        self.fields["description"].required = False