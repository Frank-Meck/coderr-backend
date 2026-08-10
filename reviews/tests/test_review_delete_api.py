from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from reviews.models import Review


class ReviewDeleteAPITest(APITestCase):
    """
    Test suite for deleting reviews through the review API.
    """

    def setUp(self):
        """
        Creates test users and a review for the test cases.
        """

        self.customer = User.objects.create_user(
            username="customer",
            password="password123",
            type="customer",
        )

        self.other_customer = User.objects.create_user(
            username="other_customer",
            password="password123",
            type="customer",
        )

        self.business = User.objects.create_user(
            username="business",
            password="password123",
            type="business",
        )

        self.review = Review.objects.create(
            business=self.business,
            reviewer=self.customer,
            rating=5,
            description="Great service",
        )

    def test_reviewer_can_delete_own_review(self):
        """
        Verifies that a reviewer can delete their own review.
        """

        self.client.force_authenticate(
            user=self.customer
        )

        url = reverse(
            "review-delete",
            kwargs={
                "pk": self.review.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Review.objects.filter(
                id=self.review.id
            ).exists()
        )

    def test_unauthenticated_user_cannot_delete_review(self):
        """
        Verifies that an unauthenticated user cannot delete a review.
        """

        url = reverse(
            "review-delete",
            kwargs={
                "pk": self.review.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_other_customer_cannot_delete_review(self):
        """
        Verifies that a customer cannot delete another customer's review.
        """

        self.client.force_authenticate(
            user=self.other_customer
        )

        url = reverse(
            "review-delete",
            kwargs={
                "pk": self.review.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_business_user_cannot_delete_review(self):
        """
        Verifies that a business user cannot delete a review.
        """

        self.client.force_authenticate(
            user=self.business
        )

        url = reverse(
            "review-delete",
            kwargs={
                "pk": self.review.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_delete_non_existing_review_returns_404(self):
        """
        Verifies that deleting a non-existent review returns a 404 response.
        """

        self.client.force_authenticate(
            user=self.customer
        )

        url = reverse(
            "review-delete",
            kwargs={
                "pk": 9999,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
