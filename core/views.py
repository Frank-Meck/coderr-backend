from django.db.models import Avg

from rest_framework.views import APIView
from rest_framework.response import Response

from .api.serializers import BaseInfoSerializer

from reviews.models import Review
from users.models import User
from offers.models import Offer


class BaseInfoView(APIView):

    def get(self, request):

        review_count = Review.objects.count()

        average_rating = Review.objects.aggregate(
            average=Avg("rating")
        )["average"]

        if average_rating is None:
            average_rating = 0.0
        else:
            average_rating = round(
                average_rating,
                1
            )

        business_profile_count = User.objects.filter(
            type="business"
        ).count()

        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }

        serializer = BaseInfoSerializer(data)

        return Response(serializer.data)