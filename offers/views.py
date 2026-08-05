from decimal import Decimal, InvalidOperation

from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.exceptions import ValidationError

from django.db.models import Q, Min, F

from offers.models import Offer
from offers.api.serializers import (
    OfferSerializer,
    OfferCreateSerializer,
)
from offers.pagination import OfferPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from offers.api.permissions import IsBusinessUser
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated


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

        min_price = self.request.query_params.get("min_price")

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
                max_delivery_time = int(max_delivery_time)
            except ValueError:
                raise ValidationError(
                    {
                        "max_delivery_time": "A valid integer is required."
                    }
                )

            queryset = queryset.filter(
                details__delivery_time_in_days__lte=max_delivery_time
            ).distinct()

        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        ordering = self.request.query_params.get("ordering")

        if ordering:

            if ordering in [
                "updated_at",
                "-updated_at",
            ]:
                queryset = queryset.order_by(ordering)

            elif ordering == "min_price":
                queryset = queryset.order_by(
                    F("min_price_value").asc(nulls_last=True)
                )

            elif ordering == "-min_price":
                queryset = queryset.order_by(
                    F("min_price_value").desc(nulls_last=True)
                )

            else:
                raise ValidationError(
                    {
                        "ordering": "Invalid ordering value."
                    }
                )

        else:
            queryset = queryset.order_by("id")

        return queryset

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        offer = serializer.save()

        response_serializer = OfferSerializer(
            offer,
            context={"request": request}
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class OfferDetailView(RetrieveAPIView):

    queryset = Offer.objects.all()

    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
