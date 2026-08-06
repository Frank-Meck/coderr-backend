from django.urls import path

from .views import (
    OrderListView,
    OrderUpdateView,
    OrderCountView
)


urlpatterns = [

    path(
        "orders/",
        OrderListView.as_view(),
        name="order-list"
    ),

    path(
        "orders/<int:pk>/",
        OrderUpdateView.as_view(),
        name="order-update"
    ),

    path(
        "order-count/<int:business_user_id>/",
        OrderCountView.as_view(),
        name="order-count"
    ),

]
