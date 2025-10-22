from django import forms
from .models import PetReport, PetSpecies, ReportType


class PetReportForm(forms.ModelForm):
    class Meta:
        model = PetReport
        fields = [
            "report_type",
            "species",
            "breed",
            "color",
            "distinctive_marks",
            "location",
            "date_seen",
            "description",
            "photo",
            "reporter_name",
            "reporter_email",
            "reporter_phone",
        ]
        widgets = {
            "date_seen": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned = super().clean()
        # Add any cross-field validation if needed
        return cleaned


class PetInquiryForm(forms.Form):
    reference_code = forms.CharField(max_length=12, label="Reference code")
    reporter_email = forms.EmailField(label="Your email")
