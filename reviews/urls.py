from django.urls import path

from .views import (
    ReviewListView,
    ReviewUpdateView
)


urlpatterns = [

    path(
        "reviews/",
        ReviewListView.as_view(),
        name="review-list"
    ),

    path(
        "reviews/<int:pk>/",
        ReviewUpdateView.as_view(),
        name="review-update"
    ),

    path(
        "reviews/<int:pk>/",
        ReviewUpdateView.as_view(),
        name="review-delete"
    ),

]
