from django.db import models
from django.conf import settings


class Review(models.Model):

    business = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_reviews",
        limit_choices_to={
            "type": "business"
        }
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_reviews",
        limit_choices_to={
            "type": "customer"
        }
    )

    rating = models.PositiveIntegerField()

    description = models.TextField(
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
                    "reviewer",
                    "business"
                ],
                name="unique_reviewer_business_review"
            )
        ]

    def __str__(self):
        return f"{self.reviewer.username} → {self.business.username} ({self.rating})"
