from decimal import Decimal, InvalidOperation

from django.db.models import F, Min, Q

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response

from offers.models import (
    Offer,
    OfferDetail,
)

from offers.pagination import OfferPagination

from offers.api.permissions import (
    IsBusinessUser,
    IsOfferOwner,
)

from offers.api.serializers import (
    OfferSerializer,
    OfferCreateSerializer,
    OfferCreateResponseSerializer,
    OfferUpdateSerializer,
    OfferUpdateResponseSerializer,
    OfferDetailResponseSerializer,
    OfferDetailSerializer,
)


class OfferListView(ListCreateAPIView):
    """
    List and create offers.

    GET requests return a filtered and ordered list of offers.
    POST requests allow authenticated business users to create a new offer.
    """

    pagination_class = OfferPagination
    serializer_class = OfferSerializer

    def get_serializer_class(self):
        """
        Return the serializer based on the current HTTP method.

        POST requests use the offer creation serializer.
        All other requests use the standard offer serializer.
        """

        if self.request.method == "POST":
            return OfferCreateSerializer

        return OfferSerializer

    def get_permissions(self):
        """
        Return permissions based on the current HTTP method.

        Creating an offer requires the user to be a business user.
        Listing offers is publicly accessible.
        """

        if self.request.method == "POST":
            return [
                IsBusinessUser()
            ]

        return [
            AllowAny()
        ]

    def get_queryset(self):
        """
        Return the offer queryset with optional filtering and ordering.

        The queryset supports filtering by creator, minimum price,
        maximum delivery time, and search terms. Results can also be
        ordered by update date or minimum offer price.
        """

        queryset = Offer.objects.annotate(
            min_price_value=Min(
                "details__price"
            )
        )

        creator_id = self.request.query_params.get(
            "creator_id"
        )

        if creator_id:

            try:
                creator_id = int(
                    creator_id
                )

            except ValueError:
                raise ValidationError(
                    {
                        "creator_id":
                        "A valid integer is required."
                    }
                )

            queryset = queryset.filter(
                business_id=creator_id
            )

        min_price = self.request.query_params.get(
            "min_price"
        )

        if min_price:

            try:
                min_price = Decimal(
                    min_price
                )

            except InvalidOperation:
                raise ValidationError(
                    {
                        "min_price":
                        "A valid number is required."
                    }
                )

            queryset = queryset.filter(
                details__price__gte=min_price
            ).distinct()

        max_delivery_time = (
            self.request.query_params.get(
                "max_delivery_time"
            )
        )

        if max_delivery_time:

            try:
                max_delivery_time = int(
                    max_delivery_time
                )

            except ValueError:
                raise ValidationError(
                    {
                        "max_delivery_time":
                        "A valid integer is required."
                    }
                )

            queryset = queryset.filter(
                details__delivery_time_in_days__lte=max_delivery_time
            ).distinct()

        search = self.request.query_params.get(
            "search"
        )

        if search:

            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
            )

        ordering = self.request.query_params.get(
            "ordering"
        )

        if ordering:

            if ordering in [
                "updated_at",
                "-updated_at",
            ]:

                queryset = queryset.order_by(
                    ordering
                )

            elif ordering == "min_price":

                queryset = queryset.order_by(
                    F(
                        "min_price_value"
                    ).asc(
                        nulls_last=True
                    )
                )

            elif ordering == "-min_price":

                queryset = queryset.order_by(
                    F(
                        "min_price_value"
                    ).desc(
                        nulls_last=True
                    )
                )

            else:

                raise ValidationError(
                    {
                        "ordering":
                        "Invalid ordering value."
                    }
                )

        else:

            queryset = queryset.order_by(
                "id"
            )

        return queryset

    def create(
        self,
        request,
        *args,
        **kwargs
    ):
        """
        Create a new offer and return the created offer data.

        The request data is validated using the creation serializer.
        A dedicated response serializer is used to return the created
        offer together with the request context.
        """

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        offer = serializer.save()

        response_serializer = (
            OfferCreateResponseSerializer(
                offer,
                context={
                    "request": request
                }
            )
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class OfferDetailView(
    RetrieveUpdateDestroyAPIView
):
    """
    Retrieve, update, or delete a single offer.

    Offers can be retrieved by authenticated users.
    Updating or deleting an offer requires the requesting user
    to be the owner of the offer.
    """

    queryset = Offer.objects.all()

    def get_permissions(self):
        """
        Return permissions based on the current HTTP method.

        PATCH and DELETE requests require authentication and offer
        ownership. GET requests only require authentication.
        """

        if self.request.method in [
            "PATCH",
            "DELETE",
        ]:

            return [
                IsAuthenticated(),
                IsOfferOwner(),
            ]

        return [
            IsAuthenticated(),
        ]

    def get_serializer_class(self):
        """
        Return the appropriate serializer for the current request.

        PATCH requests use the update serializer.
        Other requests use the detailed response serializer.
        """

        if self.request.method == "PATCH":

            return OfferUpdateSerializer

        return OfferDetailResponseSerializer

    def update(
        self,
        request,
        *args,
        **kwargs
    ):
        """
        Update an existing offer and return the updated offer data.

        The request data is validated using the update serializer.
        A dedicated response serializer is used to return the updated
        offer.
        """

        partial = kwargs.pop(
            "partial",
            False
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(
            raise_exception=True
        )

        self.perform_update(
            serializer
        )

        response_serializer = (
            OfferUpdateResponseSerializer(
                serializer.instance,
                context={
                    "request": request
                }
            )
        )

        return Response(
            response_serializer.data
        )


class OfferDetailDetailView(
    RetrieveAPIView
):
    """
    Retrieve a single offer detail.

    Access to individual offer details requires authentication.
    """

    queryset = OfferDetail.objects.all()

    serializer_class = OfferDetailSerializer

    permission_classes = [
        IsAuthenticated,
    ]