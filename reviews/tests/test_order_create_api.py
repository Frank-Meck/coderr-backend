from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from reviews.models import Review


class ReviewCreateAPITest(APITestCase):
    """
    Test suite for creating reviews through the review API.
    """

    def setUp(self):
        """
        Creates a customer and a business user for the test cases.
        """

        self.customer = User.objects.create_user(
            username="customer@test.com",
            password="test123",
            type="customer",
        )

        self.business = User.objects.create_user(
            username="business@test.com",
            password="test123",
            type="business",
        )

    def test_customer_can_create_review(self):
        """
        Verifies that an authenticated customer can create a review.
        """

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.post(
            "/api/reviews/",
            {
                "business_user": self.business.id,
                "rating": 4,
                "description": "Alles war toll!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Review.objects.count(),
            1,
        )

        review = Review.objects.first()

        self.assertEqual(
            review.business,
            self.business,
        )

        self.assertEqual(
            review.reviewer,
            self.customer,
        )

        self.assertEqual(
            review.rating,
            4,
        )

    def test_unauthenticated_user_cannot_create_review(self):
        """
        Verifies that an unauthenticated user cannot create a review.
        """

        response = self.client.post(
            "/api/reviews/",
            {
                "business_user": self.business.id,
                "rating": 4,
                "description": "Test",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_business_user_cannot_create_review(self):
        """
        Verifies that a business user cannot create a review.
        """

        self.client.force_authenticate(
            user=self.business
        )

        response = self.client.post(
            "/api/reviews/",
            {
                "business_user": self.business.id,
                "rating": 4,
                "description": "Test",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_customer_cannot_create_duplicate_review(self):
        """
        Verifies that a customer cannot review the same business twice.
        """

        Review.objects.create(
            business=self.business,
            reviewer=self.customer,
            rating=5,
            description="Erste Bewertung",
        )

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.post(
            "/api/reviews/",
            {
                "business_user": self.business.id,
                "rating": 3,
                "description": "Zweite Bewertung",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_customer_cannot_review_unknown_business(self):
        """
        Verifies that a customer cannot create a review
        for a non-existent business.
        """

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.post(
            "/api/reviews/",
            {
                "business_user": 99999,
                "rating": 4,
                "description": "Test",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
