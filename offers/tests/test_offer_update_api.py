# offers/tests/test_offer_update_api.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import User
from offers.models import Offer
from offers.models import OfferDetail


class OfferUpdateAPITest(APITestCase):

    def setUp(self):

        self.business_user = User.objects.create_user(
            username="business",
            password="password",
            type="business"
        )

        self.other_business_user = User.objects.create_user(
            username="other_business",
            password="password",
            type="business"
        )

        self.customer_user = User.objects.create_user(
            username="customer",
            password="password",
            type="customer"
        )

        self.business_token = Token.objects.create(
            user=self.business_user
        )

        self.customer_token = Token.objects.create(
            user=self.customer_user
        )

        self.offer = Offer.objects.create(
            business=self.business_user,
            title="Grafikdesign Paket",
            description="Alte Beschreibung"
        )

        self.detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=[
                "Logo Design"
            ],
            offer_type="basic"
        )

        self.url = reverse(
            "offer-detail",
            kwargs={
                "pk": self.offer.id
            }
        )


    def test_business_owner_can_update_offer(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=
            f"Token {self.business_token.key}"
        )

        response = self.client.patch(
            self.url,
            {
                "title": "Updated Grafikdesign Paket"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.offer.refresh_from_db()

        self.assertEqual(
            self.offer.title,
            "Updated Grafikdesign Paket"
        )


    def test_non_owner_cannot_update_offer(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=
            f"Token {self.customer_token.key}"
        )

        response = self.client.patch(
            self.url,
            {
                "title": "Nicht erlaubt"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            403
        )


    def test_unauthenticated_user_cannot_update_offer(self):

        response = self.client.patch(
            self.url,
            {
                "title": "Nicht erlaubt"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            401
        )


    def test_update_non_existing_offer_returns_404(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=
            f"Token {self.business_token.key}"
        )

        response = self.client.patch(
            "/api/offers/999999/",
            {
                "title": "Does not exist"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            404
        )


    def test_patch_keeps_missing_fields_unchanged(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=
            f"Token {self.business_token.key}"
        )

        response = self.client.patch(
            self.url,
            {
                "title": "Neuer Titel"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.offer.refresh_from_db()

        self.assertEqual(
            self.offer.description,
            "Alte Beschreibung"
        )


    def test_patch_updates_existing_detail_and_keeps_id(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=
            f"Token {self.business_token.key}"
        )

        old_detail_id = self.detail.id

        response = self.client.patch(
            self.url,
            {
                "details": [
                    {
                        "title": "Basic Design Updated",
                        "revisions": 3,
                        "delivery_time_in_days": 6,
                        "price": 120,
                        "features": [
                            "Logo Design",
                            "Flyer"
                        ],
                        "offer_type": "basic"
                    }
                ]
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data["details"][0]["id"],
            old_detail_id
        )

        self.detail.refresh_from_db()

        self.assertEqual(
            self.detail.title,
            "Basic Design Updated"
        )