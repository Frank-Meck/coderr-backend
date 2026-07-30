from django.db import models
from users.models import User
from offers.models import OfferDetail


class Order(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )


    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer_orders",
        limit_choices_to={
            "type": "customer"
        }
    )


    business = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="business_orders",
        limit_choices_to={
            "type": "business"
        }
    )


    offer_detail = models.ForeignKey(
        OfferDetail,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders"
    )


    offer_type = models.CharField(
        max_length=20
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


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return f"Order {self.id}"