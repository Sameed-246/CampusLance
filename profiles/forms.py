from django import forms
from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):

    class Meta:

        model = StudentProfile

        fields = [
            "college",
            "degree",
            "skills",
            "bio",
            "location",
            "github",
            "linkedin",
            "portfolio",
            "resume",
        ]

        widgets = {
            "college": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your college name"
            }),

            "degree": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your degree"
            }),

            "skills": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Python, Django, HTML, CSS, SQL"
            }),

            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Tell us about yourself"
            }),

            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your location"
            }),

            "github": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://github.com/username"
            }),

            "linkedin": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://linkedin.com/in/username"
            }),

            "portfolio": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://yourportfolio.com"
            }),

            "resume": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if user and getattr(user, "role", None) != "student":

            self.fields.pop("resume", None)