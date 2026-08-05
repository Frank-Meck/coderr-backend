from django.urls import path

from offers.views import (
    OfferListView,
    OfferDetailView,
    OfferDetailDetailView,
)


urlpatterns = [

    path(
        "offers/",
        OfferListView.as_view(),
        name="offer-list"
    ),

    path(
        "offers/<int:pk>/",
        OfferDetailView.as_view(),
        name="offer-detail"
    ),

    path(
        "offerdetails/<int:pk>/",
        OfferDetailDetailView.as_view(),
        name="offerdetail-detail"
    ),

]
