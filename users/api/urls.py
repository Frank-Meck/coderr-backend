from django.urls import path

from .views import RegistrationView, ProfileView


urlpatterns = [
    path(
        "registration/",
        RegistrationView.as_view(),
        name="registration"
    ),

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile"
    ),
]