from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from reviews.models import Review


class ReviewListAPITest(APITestCase):

    def setUp(self):

        self.customer = User.objects.create_user(
            username="customer@test.com",
            password="test123",
            type="customer"
        )

        self.other_customer = User.objects.create_user(
            username="other_customer@test.com",
            password="test123",
            type="customer"
        )

        self.business = User.objects.create_user(
            username="business@test.com",
            password="test123",
            type="business"
        )

        self.other_business = User.objects.create_user(
            username="other_business@test.com",
            password="test123",
            type="business"
        )

        self.review = Review.objects.create(
            business=self.business,
            reviewer=self.customer,
            rating=4,
            description="Sehr professioneller Service."
        )

        self.other_review = Review.objects.create(
            business=self.other_business,
            reviewer=self.other_customer,
            rating=5,
            description="Top Qualität."
        )

    def test_authenticated_user_can_get_reviews(self):

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            "/api/reviews/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            2
        )

    def test_filter_reviews_by_business_user(self):

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            f"/api/reviews/?business_user_id={self.business.id}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["business_user"],
            self.business.id
        )

    def test_filter_reviews_by_reviewer(self):

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            f"/api/reviews/?reviewer_id={self.customer.id}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["reviewer"],
            self.customer.id
        )

    def test_order_reviews_by_rating(self):

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            "/api/reviews/?ordering=rating"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        ratings = [
            review["rating"]
            for review in response.data
        ]

        self.assertEqual(
            ratings,
            sorted(ratings)
        )

    def test_unauthenticated_user_cannot_get_reviews(self):

        response = self.client.get(
            "/api/reviews/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_filter_unknown_business_returns_empty_list(self):

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            "/api/reviews/?business_user_id=99999"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data,
            []
        )
