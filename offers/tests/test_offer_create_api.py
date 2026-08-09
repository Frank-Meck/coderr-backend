"""
API tests for creating offers.

Tests offer creation, response data, authentication, user permissions,
validation of offer details, and validation of offer types.
"""

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from offers.models import Offer


class OfferCreateAPITest(APITestCase):
    """
    Test the offer creation API endpoint.
    """

    def setUp(self):
        """
        Create and authenticate a business user for the API tests.
        """

        self.business_user = User.objects.create_user(
            username="business",
            password="testpass123",
            type="business"
        )

        self.client.force_authenticate(
            user=self.business_user
        )

    def test_business_user_can_create_offer(self):
        """
        Test that an authenticated business user can create an offer.
        """

        url = reverse("offer-list")

        data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": (
                "Ein umfassendes Grafikdesign-Paket."
            ),
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                        "Logo Design"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design"
                    ],
                    "offer_type": "premium"
                }
            ]
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Offer.objects.count(),
            1
        )

        offer = Offer.objects.first()

        self.assertEqual(
            offer.details.count(),
            3
        )

    def test_business_user_receives_created_offer_with_details(self):
        """
        Test that the creation response contains the created offer and details.
        """

        url = reverse("offer-list")

        data = {
            "title": "Test Offer",
            "image": None,
            "description": "Test Beschreibung",
            "details": [
                {
                    "title": "Basic",
                    "revisions": 1,
                    "delivery_time_in_days": 3,
                    "price": 100,
                    "features": ["Feature"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 200,
                    "features": ["Feature"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium",
                    "revisions": 3,
                    "delivery_time_in_days": 7,
                    "price": 300,
                    "features": ["Feature"],
                    "offer_type": "premium"
                }
            ]
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertIn(
            "id",
            response.data
        )

        self.assertIn(
            "details",
            response.data
        )

        self.assertEqual(
            len(response.data["details"]),
            3
        )

    def test_unauthenticated_user_cannot_create_offer(self):
        """
        Test that unauthenticated users cannot create offers.
        """

        self.client.force_authenticate(
            user=None
        )

        url = reverse("offer-list")

        response = self.client.post(
            url,
            {},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def get_valid_offer_data(self):
        """
        Return valid data for creating an offer.
        """

        return {
            "title": "Test Offer",
            "image": None,
            "description": "Test Beschreibung",
            "details": [
                {
                    "title": "Basic",
                    "revisions": 1,
                    "delivery_time_in_days": 3,
                    "price": 100,
                    "features": ["Feature"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 200,
                    "features": ["Feature"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium",
                    "revisions": 3,
                    "delivery_time_in_days": 7,
                    "price": 300,
                    "features": ["Feature"],
                    "offer_type": "premium"
                }
            ]
        }

    def test_non_business_user_cannot_create_offer(self):
        """
        Test that authenticated customer users cannot create offers.
        """

        user = User.objects.create_user(
            username="customer",
            password="testpass123",
            type="customer"
        )

        self.client.force_authenticate(
            user=user
        )

        url = reverse("offer-list")

        response = self.client.post(
            url,
            self.get_valid_offer_data(),
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_offer_creation_requires_exactly_three_details(self):
        """
        Test that an offer must contain exactly three details.
        """

        url = reverse("offer-list")

        data = self.get_valid_offer_data()

        data["details"] = data["details"][:2]

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_offer_creation_rejects_duplicate_offer_types(self):
        """
        Test that duplicate offer types are rejected during creation.
        """

        url = reverse("offer-list")

        data = self.get_valid_offer_data()

        data["details"][1]["offer_type"] = "basic"

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_offer_creation_rejects_invalid_offer_type(self):
        """
        Test that invalid offer types are rejected during creation.
        """

        url = reverse("offer-list")

        data = self.get_valid_offer_data()

        data["details"][0]["offer_type"] = "gold"

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_unauthenticated_user_cannot_create_offer(self):
        """
        Test that unauthenticated users cannot create offers.
        """

        self.client.force_authenticate(
            user=None
        )

        response = self.client.post(
            reverse("offer-list"),
            self.get_valid_offer_data(),
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

