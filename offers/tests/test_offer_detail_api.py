from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from offers.models import Offer, OfferDetail


User = get_user_model()


class OfferDetailAPITest(APITestCase):

    def setUp(self):
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