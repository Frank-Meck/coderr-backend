from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .api.permissions import IsCustomer

from .models import Review

from .api.serializers import (
    ReviewSerializer,
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
)


class ReviewListView(ListCreateAPIView):
    """
    Provides endpoints for listing and creating reviews.

    Authenticated users can view reviews.
    Only authenticated customers are allowed to create reviews.
    """

    def get_permissions(self):
        """
        Returns the permissions required for the current request.

        Review creation requires the user to be authenticated
        and have customer permissions. Other requests only require
        authentication.
        """

        if self.request.method == "POST":
            return [
                IsAuthenticated(),
                IsCustomer(),
            ]

        return [
            IsAuthenticated(),
        ]

    def get_serializer_class(self):
        """
        Returns the appropriate serializer for the current request.

        The create serializer is used for POST requests.
        The default review serializer is used for other requests.
        """

        if self.request.method == "POST":
            return ReviewCreateSerializer

        return ReviewSerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new review and returns the serialized review data.
        """

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        review = serializer.save()

        response_serializer = ReviewSerializer(
            review,
            context=self.get_serializer_context(),
        )

        return Response(
            response_serializer.data,
            status=201,
        )

    def get_queryset(self):
        """
        Returns the filtered and optionally ordered review queryset.

        Reviews can be filtered by business user ID or reviewer ID.
        The results can also be ordered by rating or update time.
        """

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

        ordering = self.request.query_params.get(
            "ordering"
        )

        if ordering in [
            "updated_at",
            "-updated_at",
            "rating",
            "-rating",
        ]:
            queryset = queryset.order_by(
                ordering
            )

        return queryset


class ReviewUpdateView(
    RetrieveUpdateDestroyAPIView
):
    """
    Provides endpoints for retrieving, updating, and deleting reviews.

    Only the customer who created a review is allowed to update
    or delete it.
    """

    queryset = Review.objects.all()

    permission_classes = [
        IsAuthenticated,
    ]

    def get_serializer_class(self):
        """
        Returns the appropriate serializer for the current request.

        The update serializer is used for PUT and PATCH requests.
        The default review serializer is used for other requests.
        """

        if self.request.method in [
            "PATCH",
            "PUT",
        ]:
            return ReviewUpdateSerializer

        return ReviewSerializer

    def perform_update(
        self,
        serializer,
    ):
        """
        Updates a review if the current user is its reviewer.

        Raises PermissionDenied if the current user did not
        create the review.
        """

        review = self.get_object()

        if self.request.user != review.reviewer:
            raise PermissionDenied(
                "Only the reviewer can update this review."
            )

        serializer.save()

    def perform_destroy(
        self,
        instance,
    ):
        """
        Deletes a review if the current user is its reviewer.

        Raises PermissionDenied if the current user did not
        create the review.
        """

        if self.request.user != instance.reviewer:
            raise PermissionDenied(
                "Only the reviewer can delete this review."
            )

        instance.delete()
