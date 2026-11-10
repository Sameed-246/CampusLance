from django.db import models
from django.conf import settings


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    college = models.CharField(
        max_length=200,
        blank=True
    )

    degree = models.CharField(
        max_length=100,
        blank=True
    )

    skills = models.TextField(
        blank=True,
        help_text="Separate skills with commas"
    )

    bio = models.TextField(
        blank=True
    )

    location = models.CharField(
        max_length=100,
        blank=True
    )

    github = models.URLField(
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    portfolio = models.URLField(
        blank=True
    )

    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username