"""
Serializers for the offers API.

Defines serializers for displaying, creating, updating, and
linking offers and their associated offer details.
"""

from rest_framework import serializers

from offers.models import Offer, OfferDetail


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """
    Serialize an offer detail as a link to its detail endpoint.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "url",
        ]

    def get_url(self, obj):
        """
        Return the absolute URL of the offer detail.

        Uses the current request context when available to build
        an absolute URL. Otherwise, returns a relative API path.
        """

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(
                f"/api/offerdetails/{obj.id}/"
            )

        return f"/api/offerdetails/{obj.id}/"


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serialize the complete information of an offer detail.
    """

    class Meta:
        model = OfferDetail

        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferSerializer(serializers.ModelSerializer):
    """
    Serialize an offer for list responses.

    Includes the associated business user, linked offer details,
    minimum price, minimum delivery time, and basic user details.
    """

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
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_min_price(self, obj):
        """
        Return the lowest price among all offer details.

        Returns None if the offer has no associated details.
        """

        prices = obj.details.values_list(
            "price",
            flat=True
        )

        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        """
        Return the shortest delivery time among all offer details.

        Returns None if the offer has no associated details.
        """

        delivery_times = obj.details.values_list(
            "delivery_time_in_days",
            flat=True
        )

        return min(delivery_times) if delivery_times else None

    def get_user_details(self, obj):
        """
        Return basic information about the business user.
        """

        user = obj.business

        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        }


class OfferDetailResponseSerializer(serializers.ModelSerializer):
    """
    Serialize an offer for detailed response data.

    Includes linked offer details, minimum price, and minimum
    delivery time.
    """

    user = serializers.IntegerField(
        source="business.id",
        read_only=True
    )

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
        """
        Return the lowest price among all offer details.

        Returns None if the offer has no associated details.
        """

        prices = obj.details.values_list(
            "price",
            flat=True
        )

        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        """
        Return the shortest delivery time among all offer details.

        Returns None if the offer has no associated details.
        """

        delivery_times = obj.details.values_list(
            "delivery_time_in_days",
            flat=True
        )

        return min(delivery_times) if delivery_times else None


class OfferCreateResponseSerializer(serializers.ModelSerializer):
    """
    Serialize an offer after successful creation.

    Includes the newly created offer and all associated details.
    """

    details = OfferDetailSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Offer

        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    """
    Validate and serialize data for creating an offer detail.
    """

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
    """
    Validate and create a complete offer with its three details.

    An offer must contain exactly one basic, one standard,
    and one premium detail.
    """

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
        """
        Validate that an offer contains exactly three unique details.

        Each detail must have a unique offer type.
        """

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
        """
        Create an offer and its associated offer details.

        The business user is taken from the authenticated request.
        """

        details_data = validated_data.pop(
            "details"
        )

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


class OfferUpdateSerializer(serializers.ModelSerializer):
    """
    Validate and update an existing offer and its details.

    Offer details are optional during an update. When provided,
    each detail is updated based on its offer type.
    """

    details = OfferDetailCreateSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Offer

        fields = (
            "title",
            "image",
            "description",
            "details",
        )

    def update(self, instance, validated_data):
        """
        Update an offer and optionally update its offer details.

        Each provided detail must contain an offer type that
        matches an existing detail of the offer.
        """

        details_data = validated_data.pop(
            "details",
            None
        )

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value
            )

        instance.save()

        if details_data is not None:

            for detail_data in details_data:

                offer_type = detail_data.get(
                    "offer_type"
                )

                if not offer_type:
                    raise serializers.ValidationError(
                        {
                            "details": (
                                "offer_type is required."
                            )
                        }
                    )

                try:

                    detail = instance.details.get(
                        offer_type=offer_type
                    )

                except OfferDetail.DoesNotExist:

                    raise serializers.ValidationError(
                        {
                            "details": (
                                f"No detail with "
                                f"offer_type '{offer_type}' "
                                f"exists."
                            )
                        }
                    )

                for attr, value in detail_data.items():

                    setattr(
                        detail,
                        attr,
                        value
                    )

                detail.save()

        return instance


class OfferUpdateResponseSerializer(serializers.ModelSerializer):
    """
    Serialize an offer after a successful update.

    Includes the updated offer and all associated details.
    """

    details = OfferDetailSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Offer

        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]

