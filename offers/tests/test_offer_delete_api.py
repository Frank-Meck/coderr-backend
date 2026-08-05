from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from offers.models import Offer


User = get_user_model()


class OfferDeleteAPITest(APITestCase):

    def setUp(self):

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
