"""
URL configuration for the core project.
"""

from django.contrib import admin
from django.urls import include, path

from rest_framework.authtoken.views import obtain_auth_token

from .views import BaseInfoView


urlpatterns = [
    # Provides access to the Django admin interface.
    path(
        "admin/",
        admin.site.urls,
    ),

    # Provides an endpoint for obtaining authentication tokens.
    path(
        "api-token-auth/",
        obtain_auth_token,
    ),

    # Includes all user-related API endpoints.
    path(
        "api/",
        include("users.api.urls"),
    ),

    # Includes all offer-related API endpoints.
    path(
        "api/",
        include("offers.urls"),
    ),

    # Includes all order-related API endpoints.
    path(
        "api/",
        include("orders.urls"),
    ),

    # Includes all review-related API endpoints.
    path(
        "api/",
        include("reviews.urls"),
    ),

    # Provides general platform statistics and information.
    path(
        "api/base-info/",
        BaseInfoView.as_view(),
        name="base-info",
    ),
]
