"""
URL configuration for the users API.

Defines the endpoints for user registration, authentication,
profile management, and retrieving customer and business profiles.
"""

from django.urls import path

from .views import (
    LoginView,
    RegistrationView,
    ProfileDetailView,
    BusinessProfilesView,
    CustomerProfilesView,
)


urlpatterns = [
    # User registration and authentication
    path(
        "registration/",
        RegistrationView.as_view(),
        name="registration"
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    # Individual profile access and updates
    path(
        "profile/<int:pk>/",
        ProfileDetailView.as_view(),
        name="profile-detail"
    ),

    # Profile lists by user type
    path(
        "profiles/business/",
        BusinessProfilesView.as_view(),
        name="business-profiles"
    ),

    path(
        "profiles/customer/",
        CustomerProfilesView.as_view(),
        name="customer-profiles"
    ),
]
