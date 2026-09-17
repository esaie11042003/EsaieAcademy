from django import forms
from .models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["nom", "description"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : Mathématiques"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }