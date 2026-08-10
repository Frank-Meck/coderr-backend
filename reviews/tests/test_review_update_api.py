from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from reviews.models import Review


class ReviewUpdateAPITest(APITestCase):
    """
    Test suite for updating reviews through the review API.
    """

    def setUp(self):
        """
        Creates test users and a review used by the test cases.
        """

        self.customer = User.objects.create_user(
            username="customer@test.com",
            password="test123",
            type="customer",
        )

        self.other_customer = User.objects.create_user(
            username="other@test.com",
            password="test123",
            type="customer",
        )

        self.business = User.objects.create_user(
            username="business@test.com",
            password="test123",
            type="business",
        )

        self.review = Review.objects.create(
            business=self.business,
            reviewer=self.customer,
            rating=4,
            description="Alles war toll!",
        )

    def test_reviewer_can_update_own_review(self):
        """
        Verifies that a reviewer can update their own review.
        """

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            {
                "rating": 5,
                "description": "Noch besser als erwartet!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.review.refresh_from_db()

        self.assertEqual(
            self.review.rating,
            5,
        )

        self.assertEqual(
            self.review.description,
            "Noch besser als erwartet!",
        )

    def test_unauthenticated_user_cannot_update_review(self):
        """
        Verifies that an unauthenticated user cannot update a review.
        """

        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            {
                "rating": 5,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_other_customer_cannot_update_review(self):
        """
        Verifies that another customer cannot update someone else's review.
        """

        self.client.force_authenticate(
            user=self.other_customer
        )

        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            {
                "rating": 5,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_business_cannot_update_review(self):
        """
        Verifies that a business user cannot update a review.
        """

        self.client.force_authenticate(
            user=self.business
        )

        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            {
                "rating": 5,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_review_not_found(self):
        """
        Verifies that updating a non-existent review returns a 404 response.
        """

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.patch(
            "/api/reviews/9999/",
            {
                "rating": 5,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
