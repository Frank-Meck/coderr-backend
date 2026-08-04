from decimal import Decimal, InvalidOperation

from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError

from django.db.models import Q, Min, F

from offers.models import Offer
from offers.api.serializers import OfferSerializer
from offers.pagination import OfferPagination


class OfferListView(ListAPIView):

    pagination_class = OfferPagination
    serializer_class = OfferSerializer

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
