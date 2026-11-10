from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ["proposal"]

        widgets = {
            "proposal": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Write why you're the best candidate for this job..."
                }
            )
        }