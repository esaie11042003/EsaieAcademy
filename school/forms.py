from django import forms
from .models import SchoolYear, Period


class SchoolYearForm(forms.ModelForm):
    class Meta:
        model = SchoolYear
        fields = ["nom", "date_debut", "date_fin", "active"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : 2026-2027"}),
            "date_debut": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "date_fin": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ["school_year", "name", "start_date", "end_date", "is_active"]
        widgets = {
            "school_year": forms.Select(attrs={"class": "form-select"}),
            "name": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }