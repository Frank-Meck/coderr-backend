from rest_framework import serializers

from reviews.models import Review
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):

    business_user = serializers.IntegerField(
        source="business.id",
        read_only=True
    )

    class Meta:

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

    business_user = serializers.IntegerField(
        write_only=True
    )

    class Meta:

        model = Review

        fields = [
            "business_user",
            "rating",
            "description",
        ]

    def create(self, validated_data):

        business_user_id = validated_data.pop(
            "business_user"
        )

        try:

            business = User.objects.get(
                id=business_user_id,
                type="business"
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
            business=business
        ).exists():

            raise serializers.ValidationError(
                {
                    "detail": "You already reviewed this business."
                }
            )

        return Review.objects.create(
            business=business,
            reviewer=reviewer,
            **validated_data
        )
