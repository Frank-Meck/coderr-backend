from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .api.serializers import (
    OrderSerializer,
    OrderCreateSerializer
)


class OrderListView(ListCreateAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get_serializer_class(self):

        if self.request.method == "POST":
            return OrderCreateSerializer

        return OrderSerializer

    def get_queryset(self):

        user = self.request.user

        return (
            Order.objects.filter(
                customer=user
            )
            |
            Order.objects.filter(
                business=user
            )
        )
