from rest_framework import serializers
from rest_framework.exceptions import NotFound

from orders.models import Order
from offers.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):

    customer_user = serializers.IntegerField(
        source="customer.id",
        read_only=True
    )

    business_user = serializers.IntegerField(
        source="business.id",
        read_only=True
    )

    class Meta:

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

    offer_detail_id = serializers.IntegerField(
        write_only=True
    )

    class Meta:

        model = Order

        fields = [
            "offer_detail_id"
        ]

    def create(self, validated_data):

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
