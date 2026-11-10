from django.db import models
from accounts.models import CustomUser


class Job(models.Model):

    CATEGORY_CHOICES = [
        ('Web Development', 'Web Development'),
        ('Python', 'Python'),
        ('UI/UX', 'UI/UX'),
        ('Java', 'Java'),
        ('Cyber Security', 'Cyber Security'),
        ('Data Science', 'Data Science'),
    ]

    client = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title