from rest_framework import serializers

from reviews.models import Review
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying review data.
    """

    business_user = serializers.IntegerField(
        source="business.id",
        read_only=True,
    )

    class Meta:
        """
        Defines the model and fields used by the serializer.
        """

        model = Review

        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new reviews.

    The business is provided by its user ID. The reviewer is taken
    from the authenticated user making the request.
    """

    business_user = serializers.IntegerField(
        write_only=True,
    )

    class Meta:
        """
        Defines the model and fields required to create a review.
        """

        model = Review

        fields = [
            "business_user",
            "rating",
            "description",
        ]

    def create(self, validated_data):
        """
        Creates a new review for the specified business.

        Validates that the business exists and has the correct user type.
        Also prevents a customer from reviewing the same business more
        than once.
        """

        business_user_id = validated_data.pop(
            "business_user"
        )

        try:
            business = User.objects.get(
                id=business_user_id,
                type="business",
            )

        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "business_user": "Business user not found."
                }
            )

        reviewer = self.context["request"].user

        if Review.objects.filter(
            reviewer=reviewer,
            business=business,
        ).exists():
            raise serializers.ValidationError(
                {
                    "detail": "You already reviewed this business."
                }
            )

        return Review.objects.create(
            business=business,
            reviewer=reviewer,
            **validated_data,
        )


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying and updating existing reviews.

    Review ownership and metadata are read-only. Only the rating
    and description can be modified.
    """

    business_user = serializers.IntegerField(
        source="business.id",
        read_only=True,
    )

    class Meta:
        """
        Defines the model, fields, and read-only fields for review updates.
        """

        model = Review

        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "business_user",
            "reviewer",
            "created_at",
            "updated_at",
        ]

    def validate_rating(self, value):
        """
        Validates that the rating is between 1 and 5.
        """

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value
