
from rest_framework import serializers


class BaseInfoSerializer(serializers.Serializer):
    """
    Serializer for general platform statistics.
    """

    review_count = serializers.IntegerField()
    """
    The total number of reviews.
    """

    average_rating = serializers.FloatField()
    """
    The average rating across all reviews.
    """

    business_profile_count = serializers.IntegerField()
    """
    The total number of business profiles.
    """

    offer_count = serializers.IntegerField()
    """
    The total number of offers.
    """

