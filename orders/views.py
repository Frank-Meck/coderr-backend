from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)

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



class OrderUpdateView(RetrieveUpdateDestroyAPIView):

    queryset = Order.objects.all()


    def get_serializer_class(self):

        if self.request.method in ["PATCH", "PUT"]:
            return OrderUpdateSerializer

        return OrderSerializer


    def get_permissions(self):

        if self.request.method == "DELETE":
            return [
                IsAdminUser()
            ]

        return [
            IsAuthenticated()
        ]


    def perform_update(self, serializer):

        order = self.get_object()

        if self.request.user != order.business:

            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Only the business user can update the order."
            )


        serializer.save()