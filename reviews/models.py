from django.db import models
from django.conf import settings


class Review(models.Model):
    """
    Represents a review submitted by a customer for a business.
    Each customer can submit only one review per business.
    """

    business = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_reviews",
        limit_choices_to={
            "type": "business"
        },
    )
    """
    The business that receives the review.
    """

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_reviews",
        limit_choices_to={
            "type": "customer"
        },
    )
    """
    The customer who submitted the review.
    """

    rating = models.PositiveIntegerField()
    """
    The rating given to the business.
    """

    description = models.TextField(
        blank=True
    )
    """
    An optional written description of the review.
    """

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    """
    The date and time when the review was created.
    """

    updated_at = models.DateTimeField(
        auto_now=True
    )
    """
    The date and time when the review was last updated.
    """

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
        """
        Ensures that a customer can review a business only once.
        """

    def __str__(self):
        return f"{self.reviewer.username} → {self.business.username} ({self.rating})"
