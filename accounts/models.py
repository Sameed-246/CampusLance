from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('client', 'Client'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Basic Information
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )

    # Student Information
    college = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)

    # Professional Information
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)

    # Social Links
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)

    # Resume
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    # About
    about = models.TextField(blank=True)

    def __str__(self):
        return self.username