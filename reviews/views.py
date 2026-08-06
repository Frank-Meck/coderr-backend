from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Review
from .api.serializers import ReviewSerializer


class ReviewListView(ListAPIView):

    serializer_class = ReviewSerializer

    permission_classes = [
        IsAuthenticated
    ]

    ordering_fields = [
        "updated_at",
        "rating"
    ]

    def get_queryset(self):

        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get(
            "business_user_id"
        )

        reviewer_id = self.request.query_params.get(
            "reviewer_id"
        )

        if business_user_id:
            queryset = queryset.filter(
                business_id=business_user_id
            )

        if reviewer_id:
            queryset = queryset.filter(
                reviewer_id=reviewer_id
            )

        return queryset