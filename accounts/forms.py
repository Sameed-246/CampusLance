from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'role',
            'profile_image',
            'password1',
            'password2',
        ]