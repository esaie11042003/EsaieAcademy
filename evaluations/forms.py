from django import forms
from .models import Evaluation
from assignments.models import Assignment


class EvaluationForm(forms.ModelForm):

    class Meta:
        model = Evaluation
        fields = ["assignment", "period", "evaluation_type", "numero", "date", "note_sur"]
        widgets = {
            "assignment": forms.Select(attrs={"class": "form-select"}),
            "period": forms.Select(attrs={"class": "form-select"}),
            "evaluation_type": forms.Select(attrs={"class": "form-select"}),
            "numero": forms.NumberInput(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "note_sur": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields["assignment"].queryset = Assignment.objects.filter(teacher=teacher, active=True)


class ModifierNoteForm(forms.Form):
    note = forms.DecimalField(
        label="Note",
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"})
    )
    absent = forms.BooleanField(
        label="Absent",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    raison = forms.CharField(
        label="Raison de la modification",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        required=True
    )


class SupprimerNoteForm(forms.Form):
    raison = forms.CharField(
        label="Raison de la suppression",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        required=True
    )