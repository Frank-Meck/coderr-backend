from rest_framework import status
from django.urls import reverse

from rest_framework.test import APITestCase

from users.models import User
from offers.models import Offer, OfferDetail
from reviews.models import Review


class BaseInfoAPITest(APITestCase):
    """
    Test suite for the base information API endpoint.
    """

    def setUp(self):
        """
        Creates test users, offers, offer details, and reviews
        required for the test cases.
        """

        self.business_1 = User.objects.create_user(
            username="business1",
            password="test123",
            type="business",
        )

        self.business_2 = User.objects.create_user(
            username="business2",
            password="test123",
            type="business",
        )

        self.customer = User.objects.create_user(
            username="customer1",
            password="test123",
            type="customer",
        )

        # Create test offers.

        self.offer_1 = Offer.objects.create(
            business=self.business_1,
            title="Website Design",
            description="Modern website",
        )

        self.offer_2 = Offer.objects.create(
            business=self.business_2,
            title="SEO Service",
            description="SEO optimization",
        )

        # Create offer details.

        OfferDetail.objects.create(
            offer=self.offer_1,
            offer_type="basic",
            title="Basic",
            price=100,
            delivery_time_in_days=5,
            revisions=2,
        )

        OfferDetail.objects.create(
            offer=self.offer_2,
            offer_type="premium",
            title="Premium",
            price=500,
            delivery_time_in_days=10,
            revisions=5,
        )

        # Create reviews.

        Review.objects.create(
            business=self.business_1,
            reviewer=self.customer,
            rating=5,
            description="Great service",
        )

        Review.objects.create(
            business=self.business_2,
            reviewer=self.customer,
            rating=4,
            description="Good service",
        )

    def test_base_info_returns_correct_statistics(self):
        """
        Verifies that the base information endpoint returns
        the correct platform statistics.
        """

        url = reverse("base-info")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["review_count"],
            2,
        )

        self.assertEqual(
            response.data["business_profile_count"],
            2,
        )

        self.assertEqual(
            response.data["offer_count"],
            2,
        )

        self.assertEqual(
            response.data["average_rating"],
            4.5,
        )

    def test_base_info_returns_zero_when_no_data_exists(self):
        """
        Verifies that the base information endpoint returns zero values
        when no relevant data exists.
        """

        Review.objects.all().delete()
        User.objects.all().delete()
        Offer.objects.all().delete()

        response = self.client.get(
            reverse("base-info")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["review_count"],
            0,
        )

        self.assertEqual(
            response.data["average_rating"],
            0.0,
        )

        self.assertEqual(
            response.data["business_profile_count"],
            0,
        )

        self.assertEqual(
            response.data["offer_count"],
            0,
        )
