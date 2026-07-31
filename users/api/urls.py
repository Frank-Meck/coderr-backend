from django.urls import path

from .views import LoginView, RegistrationView, ProfileView


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
        "profile/",
        ProfileView.as_view(),
        name="profile"
    ),
]
