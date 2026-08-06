from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from reviews.models import Review


class ReviewDeleteAPITest(APITestCase):

    def setUp(self):

        self.customer = User.objects.create_user(
            username="customer",
            password="password123",
            type="customer"
        )

        self.other_customer = User.objects.create_user(
            username="other_customer",
            password="password123",
            type="customer"
        )

        self.business = User.objects.create_user(
            username="business",
            password="password123",
            type="business"
        )

        self.review = Review.objects.create(
            business=self.business,
            reviewer=self.customer,
            rating=5,
            description="Great service"
        )

    def test_reviewer_can_delete_own_review(self):

        self.client.force_authenticate(
            user=self.customer
        )

        url = reverse(
            "review-delete",
            kwargs={
                "pk": self.review.id
            }
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Review.objects.filter(
                id=self.review.id
            ).exists()
        )

    def test_unauthenticated_user_cannot_delete_review(self):

        url = reverse(
            "review-delete",
            kwargs={
                "pk": self.review.id
            }
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_other_customer_cannot_delete_review(self):

        self.client.force_authenticate(
            user=self.other_customer
        )

        url = reverse(
            "review-delete",
            kwargs={
                "pk": self.review.id
            }
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_business_user_cannot_delete_review(self):

        self.client.force_authenticate(
            user=self.business
        )

        url = reverse(
            "review-delete",
            kwargs={
                "pk": self.review.id
            }
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_delete_non_existing_review_returns_404(self):

        self.client.force_authenticate(
            user=self.customer
        )

        url = reverse(
            "review-delete",
            kwargs={
                "pk": 9999
            }
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
