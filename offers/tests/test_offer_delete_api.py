"""
API tests for deleting offers.

Tests offer deletion permissions, authentication requirements,
successful deletion by the offer owner, and handling of
non-existing offers.
"""

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from offers.models import Offer


User = get_user_model()


class OfferDeleteAPITest(APITestCase):
    """
    Test the offer deletion API endpoint.
    """

    def setUp(self):
        """
        Create business and customer users and a test offer.
        """

        self.business = User.objects.create_user(
            username="business@test.de",
            password="test12345",
            type="business"
        )

        self.customer = User.objects.create_user(
            username="customer@test.de",
            password="test12345",
            type="customer"
        )

        self.offer = Offer.objects.create(
            business=self.business,
            title="Test Angebot",
            description="Beschreibung"
        )

    def test_business_owner_can_delete_offer(self):
        """
        Test that the business owner can successfully delete an offer.
        """

        self.client.force_authenticate(
            user=self.business
        )

        response = self.client.delete(
            f"/api/offers/{self.offer.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Offer.objects.filter(
                id=self.offer.id
            ).exists()
        )

    def test_customer_cannot_delete_offer(self):
        """
        Test that a customer cannot delete an offer.
        """

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.delete(
            f"/api/offers/{self.offer.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertTrue(
            Offer.objects.filter(
                id=self.offer.id
            ).exists()
        )

    def test_unauthenticated_user_cannot_delete_offer(self):
        """
        Test that unauthenticated users cannot delete an offer.
        """

        response = self.client.delete(
            f"/api/offers/{self.offer.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertTrue(
            Offer.objects.filter(
                id=self.offer.id
            ).exists()
        )

    def test_delete_non_existing_offer_returns_404(self):
        """
        Test that deleting a non-existing offer returns a 404 response.
        """

        self.client.force_authenticate(
            user=self.business
        )

        response = self.client.delete(
            "/api/offers/99999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
