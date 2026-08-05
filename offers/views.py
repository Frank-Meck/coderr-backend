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
    OfferUpdateSerializer,
    OfferDetailSerializer,
)


class OfferListView(ListCreateAPIView):

    pagination_class = OfferPagination
    serializer_class = OfferSerializer

    def get_permissions(self):

        if self.request.method == "POST":
            return [
                IsBusinessUser()
            ]

        return [
            AllowAny()
        ]

    def get_serializer_class(self):

        if self.request.method == "POST":
            return OfferCreateSerializer

        return OfferSerializer

    def get_queryset(self):

        queryset = Offer.objects.annotate(
            min_price_value=Min("details__price")
        )

        creator_id = self.request.query_params.get("creator_id")

        if creator_id:
            try:
                creator_id = int(creator_id)

            except ValueError:
                raise ValidationError(
                    {
                        "creator_id": "A valid integer is required."
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
                min_price = Decimal(min_price)

            except InvalidOperation:
                raise ValidationError(
                    {
                        "min_price": "A valid number is required."
                    }
                )

            queryset = queryset.filter(
                details__price__gte=min_price
            ).distinct()

        max_delivery_time = self.request.query_params.get(
            "max_delivery_time"
        )

        if max_delivery_time:

            try:
                max_delivery_time = int(
                    max_delivery_time
                )

            except ValueError:
                raise ValidationError(
                    {
                        "max_delivery_time": "A valid integer is required."
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
                    F("min_price_value").asc(
                        nulls_last=True
                    )
                )

            elif ordering == "-min_price":

                queryset = queryset.order_by(
                    F("min_price_value").desc(
                        nulls_last=True
                    )
                )

            else:
                raise ValidationError(
                    {
                        "ordering": "Invalid ordering value."
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

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        offer = serializer.save()

        response_serializer = OfferSerializer(
            offer,
            context={
                "request": request
            }
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class OfferDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Offer.objects.all()

    permission_classes = [
        IsAuthenticated,
        IsOfferOwner,
    ]

    def get_serializer_class(self):

        if self.request.method == "PATCH":

            return OfferUpdateSerializer

        return OfferSerializer

    def update(
        self,
        request,
        *args,
        **kwargs
    ):

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

        response_serializer = OfferSerializer(
            serializer.instance,
            context={
                "request": request
            }
        )

        return Response(
            response_serializer.data
        )


class OfferDetailDetailView(RetrieveAPIView):

    queryset = OfferDetail.objects.all()

    serializer_class = OfferDetailSerializer

    permission_classes = [
        IsAuthenticated,
    ]
