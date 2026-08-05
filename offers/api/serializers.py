from rest_framework import serializers

from offers.models import Offer, OfferDetail


class OfferDetailLinkSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "url",
        ]

    def get_url(self, obj):

        return f"/offerdetails/{obj.id}/"


class OfferSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(
        source="business.id",
        read_only=True
    )

    user_details = serializers.SerializerMethodField()

    details = OfferDetailLinkSerializer(
        many=True,
        read_only=True
    )

    min_price = serializers.SerializerMethodField()

    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "user_details",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
        ]

    def get_min_price(self, obj):

        prices = obj.details.values_list(
            "price",
            flat=True
        )

        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):

        delivery_times = obj.details.values_list(
            "delivery_time_in_days",
            flat=True
        )

        return min(delivery_times) if delivery_times else None

    def get_user_details(self, obj):

        user = obj.business

        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        }


class OfferDetailCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetail
        fields = (
            "title",
            "price",
            "delivery_time_in_days",
            "revisions",
            "features",
            "offer_type",
        )


class OfferCreateSerializer(serializers.ModelSerializer):

    details = OfferDetailCreateSerializer(
        many=True
    )

    class Meta:
        model = Offer
        fields = (
            "title",
            "image",
            "description",
            "details",
        )

    def validate_details(self, value):

        if len(value) != 3:
            raise serializers.ValidationError(
                "An offer must have exactly three details."
            )

        offer_types = [
            detail["offer_type"]
            for detail in value
        ]

        if len(set(offer_types)) != 3:
            raise serializers.ValidationError(
                "Offer types must be unique."
            )

        return value


    def create(self, validated_data):

        details_data = validated_data.pop("details")

        offer = Offer.objects.create(
            business=self.context["request"].user,
            **validated_data
        )

        for detail_data in details_data:
            OfferDetail.objects.create(
                offer=offer,
                **detail_data
            )

        return offer
