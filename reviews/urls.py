from django.urls import path

from .views import (
    ReviewListView,
    ReviewUpdateView,
)


urlpatterns = [
    # Displays a list of all reviews.
    path(
        "reviews/",
        ReviewListView.as_view(),
        name="review-list",
    ),

    # Retrieves or updates an existing review.
    path(
        "reviews/<int:pk>/",
        ReviewUpdateView.as_view(),
        name="review-update",
    ),

    # Deletes an existing review.
    path(
        "reviews/<int:pk>/delete/",
        ReviewUpdateView.as_view(),
        name="review-delete",
    ),
]
