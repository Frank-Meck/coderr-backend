from django.urls import path

from .views import (
    OrderListView,
    OrderUpdateView
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

]