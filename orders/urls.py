from django.urls import path

from .views import (
    OrderListView,
    OrderUpdateView,
    OrderCountView,
    CompletedOrderCountView
)


urlpatterns = [

    # List all orders related to the authenticated user
    # and create a new order
    path(
        "orders/",
        OrderListView.as_view(),
        name="order-list"
    ),

    # Retrieve, update, or delete a specific order
    path(
        "orders/<int:pk>/",
        OrderUpdateView.as_view(),
        name="order-update"
    ),

    # Return the number of orders currently in progress
    # for a specific business user
    path(
        "order-count/<int:business_user_id>/",
        OrderCountView.as_view(),
        name="order-count"
    ),

    # Return the number of completed orders
    # for a specific business user
    path(
        "completed-order-count/<int:business_user_id>/",
        CompletedOrderCountView.as_view(),
        name="completed-order-count"
    ),
]

