"""
Database models for the offers API.

Defines the models for offers and their associated details,
including pricing, delivery times, revisions, and features.
"""

from django.db import models

from users.models import User


class Offer(models.Model):
    """
    Represent an offer created by a business user.

    An offer contains general information such as its title,
    image, description, and timestamps. Each offer belongs
    to a business user.
    """

    business = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="offers",
        limit_choices_to={
            "type": "business"
        }
    )

    title = models.CharField(
        max_length=255
    )

    image = models.ImageField(
        upload_to="offers/",
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        """
        Return the title of the offer as its string representation.
        """

        return self.title


class OfferDetail(models.Model):
    """
    Represent a specific package or pricing tier of an offer.

    Each offer detail defines an offer type, price, delivery time,
    number of revisions, and additional features. An offer can have
    only one detail for each offer type.
    """

    OFFER_TYPES = (
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    )

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="details"
    )

    offer_type = models.CharField(
        max_length=20,
        choices=OFFER_TYPES
    )

    title = models.CharField(
        max_length=255
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    delivery_time_in_days = models.PositiveIntegerField()

    revisions = models.PositiveIntegerField(
        default=0
    )

    features = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "offer",
                    "offer_type"
                ],
                name="unique_offer_detail_type"
            )
        ]

    def __str__(self):
        """
        Return the offer title and offer type as a string representation.
        """

        return f"{self.offer.title} - {self.offer_type}"

