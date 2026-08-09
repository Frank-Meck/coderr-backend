"""
URL configuration for the offers API.

Defines the endpoints for listing, creating, retrieving,
updating, and deleting offers, as well as retrieving
individual offer details.
"""

from django.urls import path

from offers.views import (
    OfferListView,
    OfferDetailView,
    OfferDetailDetailView,
)

urlpatterns = [


    # Offer list and creation
    path(
        "offers/",
        OfferListView.as_view(),
        name="offer-list"
    ),

    # Individual offer access and updates
    path(
        "offers/<int:pk>/",
        OfferDetailView.as_view(),
        name="offer-detail"
    ),

    # Individual offer detail access
    path(
        "offerdetails/<int:pk>/",
        OfferDetailDetailView.as_view(),
        name="offerdetail-detail"
    ),


]
