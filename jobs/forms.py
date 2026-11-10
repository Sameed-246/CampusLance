from django import forms
from .models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job

        fields = [
            'title',
            'category',
            'description',
            'budget',
            'deadline',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the job requirements',
                'rows': 6
            }),

            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your budget'
            }),

            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }