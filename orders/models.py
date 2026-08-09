from django.db import models

from users.models import User
from offers.models import OfferDetail


class Order(models.Model):
    """
    Represents an order placed by a customer for a business service.

    An order is associated with a customer, a business user, and
    optionally an offer detail. It stores the selected service,
    pricing information, delivery time, revisions, features,
    and the current order status.
    """

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    # Customer who placed the order
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer_orders",
        limit_choices_to={
            "type": "customer"
        }
    )

    # Business user responsible for the order
    business = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="business_orders",
        limit_choices_to={
            "type": "business"
        }
    )

    # Optional reference to the selected offer detail
    offer_detail = models.ForeignKey(
        OfferDetail,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders"
    )

    # Type of the selected offer
    offer_type = models.CharField(
        max_length=20
    )

    # Title of the ordered service
    title = models.CharField(
        max_length=255
    )

    # Price of the order
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Number of days required for delivery
    delivery_time_in_days = models.PositiveIntegerField()

    # Number of revisions included in the order
    revisions = models.PositiveIntegerField(
        default=0
    )

    # Additional features included in the order
    features = models.JSONField(
        default=dict,
        blank=True
    )

    # Current status of the order
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # Timestamp when the order was created
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Timestamp when the order was last updated
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        """
        Return a human-readable representation of the order.
        """
        return f"Order {self.id}"

