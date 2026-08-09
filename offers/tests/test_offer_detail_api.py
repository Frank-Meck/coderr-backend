"""
API tests for retrieving offers.

Tests authenticated offer retrieval, authentication requirements,
offer details, calculated minimum values, and handling of
non-existing offers.
"""

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from offers.models import Offer, OfferDetail


User = get_user_model()


class OfferDetailAPITest(APITestCase):
    """
    Test the API endpoint for retrieving individual offers.
    """

    def setUp(self):
        """
        Create a business user, an offer, and its associated details.
        """

        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@test.de",
            password="testpassword123",
            type="business"
        )

        self.offer = Offer.objects.create(
            business=self.business_user,
            title="Grafikdesign-Paket",
            description="Ein Grafikdesign Angebot"
        )

        OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Design",
            revisions=1,
            delivery_time_in_days=5,
            price=50,
            features=[
                "Logo Design"
            ],
            offer_type="basic"
        )

        OfferDetail.objects.create(
            offer=self.offer,
            title="Standard Design",
            revisions=2,
            delivery_time_in_days=7,
            price=100,
            features=[
                "Logo Design",
                "Flyer"
            ],
            offer_type="standard"
        )

        OfferDetail.objects.create(
            offer=self.offer,
            title="Premium Design",
            revisions=5,
            delivery_time_in_days=10,
            price=200,
            features=[
                "Komplettes Branding"
            ],
            offer_type="premium"
        )

    def test_get_offer_authenticated(self):
        """
        Test that an authenticated user can retrieve an offer.

        The response must contain the offer data, all associated
        details, minimum price, and minimum delivery time.
        """

        self.client.force_authenticate(
            user=self.business_user
        )

        url = reverse(
            "offer-detail",
            kwargs={
                "pk": self.offer.id
            }
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["id"],
            self.offer.id
        )

        self.assertEqual(
            response.data["title"],
            "Grafikdesign-Paket"
        )

        self.assertEqual(
            len(response.data["details"]),
            3
        )

        self.assertIn(
            "min_price",
            response.data
        )

        self.assertIn(
            "min_delivery_time",
            response.data
        )

    def test_get_offer_without_authentication(self):
        """
        Test that unauthenticated users cannot retrieve an offer.
        """

        url = reverse(
            "offer-detail",
            kwargs={
                "pk": self.offer.id
            }
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_get_non_existing_offer(self):
        """
        Test that retrieving a non-existing offer returns a 404 response.
        """

        self.client.force_authenticate(
            user=self.business_user
        )

        url = reverse(
            "offer-detail",
            kwargs={
                "pk": 999999
            }
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
