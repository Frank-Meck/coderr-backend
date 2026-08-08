from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model extending Django's default AbstractUser.

    Stores authentication data together with the user's account type
    and creation/update timestamps. Users can be registered as either
    customers or business accounts.
    """

    USER_TYPES = (
        ("customer", "Customer"),
        ("business", "Business"),
    )

    type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default="customer",
        help_text="Defines whether the user is a customer or business account.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the user account was created.",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the user account was last updated.",
    )

    def __str__(self):
        """
        Return the username as the string representation of the user.

        Returns:
            str: The username of the user.
        """
        return self.username


class Profile(models.Model):
    """
    Extended profile information linked to a user.

    Stores personal and business-related profile information such as
    contact details, profile image, location, description, and working hours.
    Each user can have exactly one associated profile.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="User account associated with this profile.",
    )

    first_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="User's first name.",
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="User's last name.",
    )

    file = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
        help_text="Profile image uploaded by the user.",
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the profile image was uploaded.",
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="User's location or address information.",
    )

    tel = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="User's telephone number.",
    )

    description = models.TextField(
        blank=True,
        default="",
        help_text="Short description or biography of the user.",
    )

    working_hours = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="User's working hours.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the profile was created.",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the profile was last updated.",
    )

    def __str__(self):
        """
        Return the full name of the profile owner.

        Returns:
            str: The first and last name of the user.
        """
        return f"{self.first_name} {self.last_name}"
