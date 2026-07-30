from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER_TYPES = (
        ("customer", "Customer"),
        ("business", "Business"),
    )

    type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default="customer"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.username


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    first_name = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    file = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    tel = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    description = models.TextField(
        blank=True,
        default=""
    )

    working_hours = models.JSONField(
        blank=True,
        default=dict
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} Profile"
