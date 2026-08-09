from rest_framework import serializers
from rest_framework.exceptions import NotFound

from orders.models import Order
from offers.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for representing order data in API responses.

    Customer and business user IDs are exposed as read-only fields.
    """

    customer_user = serializers.IntegerField(
        source="customer.id",
        read_only=True
    )

    business_user = serializers.IntegerField(
        source="business.id",
        read_only=True
    )

    class Meta:
        """
        Define the model and fields included in the serialized data.
        """

        model = Order

        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used to create a new order from an offer detail.

    The client only needs to provide the ID of the selected offer detail.
    The remaining order data is taken from the corresponding OfferDetail.
    """

    offer_detail_id = serializers.IntegerField(
        write_only=True
    )

    class Meta:
        """
        Define the model and fields required to create an order.
        """

        model = Order

        fields = [
            "offer_detail_id"
        ]

    def create(self, validated_data):
        """
        Create a new order based on the selected offer detail.

        The offer detail is looked up using the provided ID. The current
        authenticated user is assigned as the customer, while the
        business user and order details are taken from the offer detail.

        Raises:
            NotFound: If the specified offer detail does not exist.
        """
        offer_detail_id = validated_data.pop(
            "offer_detail_id"
        )

        try:
            offer_detail = OfferDetail.objects.get(
                id=offer_detail_id
            )

        except OfferDetail.DoesNotExist:
            raise NotFound(
                "OfferDetail not found."
            )

        customer = self.context["request"].user

        return Order.objects.create(
            customer=customer,

            business=offer_detail.offer.business,

            offer_detail=offer_detail,

            title=offer_detail.title,

            revisions=offer_detail.revisions,

            delivery_time_in_days=offer_detail.delivery_time_in_days,

            price=offer_detail.price,

            features=offer_detail.features,

            offer_type=offer_detail.offer_type,

            status="in_progress"
        )


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer used to update an existing order.

    Order information such as the customer, business, title, price,
    and delivery details is read-only. Only fields that are not
    explicitly marked as read-only can be modified.
    """

    customer_user = serializers.IntegerField(
        source="customer.id",
        read_only=True
    )

    business_user = serializers.IntegerField(
        source="business.id",
        read_only=True
    )

    class Meta:
        """
        Define the model, fields, and read-only fields for order updates.
        """

        model = Order

        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "created_at",
            "updated_at",
        ]

