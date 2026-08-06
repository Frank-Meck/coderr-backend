from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from users.models import User

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


class OrderCountView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, business_user_id):

        business_user = get_object_or_404(
            User,
            id=business_user_id,
            type="business"
        )

        count = Order.objects.filter(
            business=business_user,
            status="in_progress"
        ).count()

        return Response(
            {
                "order_count": count
            },
            status=status.HTTP_200_OK
        )
