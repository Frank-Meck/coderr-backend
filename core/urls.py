
"""
URL configuration for core project.
"""

from django.contrib import admin
from django.urls import include, path

from rest_framework.authtoken.views import obtain_auth_token

from .views import BaseInfoView


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "api-token-auth/",
        obtain_auth_token,
    ),

    path(
        "api/",
        include("users.api.urls")
    ),

    path(
        "api/",
        include("offers.urls")
    ),

    path(
        "api/",
        include("orders.urls")
    ),

    path(
        "api/",
        include("reviews.urls")
    ),

    path(
        "api/base-info/",
        BaseInfoView.as_view(),
        name="base-info"
    ),

]
