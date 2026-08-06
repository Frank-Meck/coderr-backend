from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import IsAuthenticated

from rest_framework.exceptions import PermissionDenied

from .api.permissions import IsCustomer

from .models import Review

from .api.serializers import (
    ReviewSerializer,
    ReviewCreateSerializer,
    ReviewUpdateSerializer
)


class ReviewListView(ListCreateAPIView):

    def get_permissions(self):

        if self.request.method == "POST":
            return [
                IsCustomer()
            ]

        return [
            IsAuthenticated()
        ]

    def get_serializer_class(self):

        if self.request.method == "POST":
            return ReviewCreateSerializer

        return ReviewSerializer

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


class ReviewUpdateView(RetrieveUpdateDestroyAPIView):

    queryset = Review.objects.all()

    permission_classes = [
        IsAuthenticated
    ]

    def get_serializer_class(self):

        if self.request.method in [
            "PATCH",
            "PUT"
        ]:

            return ReviewUpdateSerializer

        return ReviewSerializer

    def perform_update(self, serializer):

        review = self.get_object()

        if self.request.user != review.reviewer:

            raise PermissionDenied(
                "Only the reviewer can update this review."
            )

        serializer.save()

    def perform_destroy(self, instance):

        if self.request.user != instance.reviewer:

            raise PermissionDenied(
                "Only the reviewer can delete this review."
            )

        instance.delete()
