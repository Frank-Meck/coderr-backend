from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from offers.models import Offer, OfferDetail


class OfferDetailDetailAPITest(APITestCase):

    def setUp(self):

        self.business = User.objects.create_user(
            username="business_test",
            password="testpass123",
            type="business",
        )

        self.customer = User.objects.create_user(
            username="customer_test",
            password="testpass123",
            type="customer",
        )

        self.offer = Offer.objects.create(
            business=self.business,
            title="Website Design",
            description="Design Angebot",
        )

        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=[
                "Logo Design",
                "Visitenkarte",
            ],
            offer_type="basic",
        )

        self.url = reverse(
            "offerdetail-detail",
            kwargs={
                "pk": self.offer_detail.id
            }
        )

    def test_authenticated_user_can_get_offer_detail(self):

        self.client.force_authenticate(
            user=self.business
        )

        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["id"],
            self.offer_detail.id
        )

        self.assertEqual(
            response.data["offer_type"],
            "basic"
        )

    def test_customer_can_get_offer_detail(self):

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_offer_detail_without_token_returns_401(self):

        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_get_non_existing_offer_detail_returns_404(self):

        self.client.force_authenticate(
            user=self.business
        )

        url = reverse(
            "offerdetail-detail",
            kwargs={
                "pk": 999999
            }
        )

        response = self.client.get(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
