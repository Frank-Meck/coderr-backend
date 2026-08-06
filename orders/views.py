from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.permissions import IsAuthenticated

from .api.permissions import IsCustomer

from .models import Order

from .api.serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderUpdateSerializer
)


class OrderListView(ListCreateAPIView):

    def get_permissions(self):

        if self.request.method == "POST":
            return [IsCustomer()]

        return [IsAuthenticated()]


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


class OrderUpdateView(RetrieveUpdateAPIView):

    queryset = Order.objects.all()

    serializer_class = OrderUpdateSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def perform_update(self, serializer):

        order = self.get_object()

        if self.request.user != order.business:

            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Only the business user can update the order."
            )


        serializer.save()