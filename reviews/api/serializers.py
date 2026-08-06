from rest_framework import serializers

from reviews.models import Review


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
        