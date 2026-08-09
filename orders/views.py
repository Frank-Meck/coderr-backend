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
    """
    Handles listing existing orders and creating new orders.

    Authenticated users can retrieve orders related to them.
    Customer users are allowed to create new orders.
    """

    def get_permissions(self):
        """
        Return the permissions required for the current request.

        Customers are required to create orders, while authenticated
        users are allowed to retrieve the order list.
        """
        if self.request.method == "POST":
            return [IsCustomer()]

        return [IsAuthenticated()]

    def get_serializer_class(self):
        """
        Return the serializer class based on the request method.

        Uses the creation serializer for POST requests and the
        standard order serializer for other requests.
        """
        if self.request.method == "POST":
            return OrderCreateSerializer

        return OrderSerializer

    def get_queryset(self):
        """
        Return orders related to the currently authenticated user.

        Users can access orders where they are either the customer
        or the business user.
        """
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

    def create(self, request, *args, **kwargs):
        """
        Create a new order and return the created order.

        The request data is validated using the creation serializer.
        The created order is then serialized using the standard
        order serializer for the response.
        """
        # Validate request data
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        # Create the order
        order = serializer.save()

        # Serialize the created order with the standard
        # OrderSerializer for the response
        response_serializer = OrderSerializer(
            order,
            context={
                "request": request
            }
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class OrderUpdateView(RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a single order.

    Authenticated users can retrieve and update orders.
    Only admin users are allowed to delete orders.
    """

    queryset = Order.objects.all()

    def get_serializer_class(self):
        """
        Return the appropriate serializer for the request method.

        Uses the update serializer for PUT and PATCH requests
        and the standard order serializer for GET requests.
        """
        if self.request.method in ["PATCH", "PUT"]:
            return OrderUpdateSerializer

        return OrderSerializer

    def get_permissions(self):
        """
        Return the permissions required for the current request.

        Only admin users are allowed to delete orders.
        All other supported requests require authentication.
        """
        if self.request.method == "DELETE":
            return [
                IsAdminUser()
            ]

        return [
            IsAuthenticated()
        ]

    def perform_update(self, serializer):
        """
        Update an order if the current user is the business user.

        Only the business user associated with the order is allowed
        to update it.
        """
        order = self.get_object()

        if self.request.user != order.business:

            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Only the business user can update the order."
            )

        serializer.save()


class OrderCountView(APIView):
    """
    Return the number of orders currently in progress
    for a specific business user.
    """

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, business_user_id):
        """
        Return the number of in-progress orders for a business user.

        The business user is identified by the provided user ID.
        """
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


class CompletedOrderCountView(APIView):
    """
    Return the number of completed orders for a specific
    business user.
    """

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, business_user_id):
        """
        Return the number of completed orders for a business user.

        The business user is identified by the provided user ID.
        """
        business_user = get_object_or_404(
            User,
            id=business_user_id,
            type="business"
        )

        count = Order.objects.filter(
            business=business_user,
            status="completed"
        ).count()

        return Response(
            {
                "completed_order_count": count
            },
            status=status.HTTP_200_OK
        )

