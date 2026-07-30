from django.db import models
from users.models import User


class Offer(models.Model):

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
        return self.title


class OfferDetail(models.Model):

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
        return f"{self.offer.title} - {self.offer_type}"
