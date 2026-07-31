from django.urls import path

from .views import (
    LoginView,
    RegistrationView,
    ProfileDetailView,
    BusinessProfilesView,
    CustomerProfilesView,
)


urlpatterns = [

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

    path(
        "profile/<int:pk>/",
        ProfileDetailView.as_view(),
        name="profile-detail"
    ),

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
