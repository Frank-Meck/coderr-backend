"""
API tests for listing offers.

Tests offer listing, pagination, response fields, filtering,
searching, and ordering of offers.
"""

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from offers.models import Offer, OfferDetail


class OfferListAPITest(APITestCase):
    """
    Test the offer list API endpoint.
    """

    def setUp(self):
        """
        Create business users, offers, and an offer detail for the tests.
        """

        self.business_user = User.objects.create_user(
            username="business1",
            password="testpass123",
            type="business"
        )

        self.other_business_user = User.objects.create_user(
            username="business2",
            password="testpass123",
            type="business"
        )

        self.offer = Offer.objects.create(
            business=self.business_user,
            title="Website Design",
            description="Professionelles Webdesign"
        )

        self.other_offer = Offer.objects.create(
            business=self.other_business_user,
            title="Logo Design",
            description="Professionelles Logo"
        )

        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            offer_type="basic",
            title="Basic Package",
            price=100,
            delivery_time_in_days=7
        )

    def test_get_offers_list(self):
        """
        Test that the offer list endpoint returns a successful response.
        """

        url = reverse("offer-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_offers_contains_created_offer(self):
        """
        Test that the created offer is included in the offer list.
        """

        url = reverse("offer-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        results = response.data["results"]

        offer_ids = [
            offer["id"]
            for offer in results
        ]

        self.assertIn(
            self.offer.id,
            offer_ids
        )

    def test_get_offers_uses_pagination(self):
        """
        Test that the offer list response contains pagination fields.
        """

        url = reverse("offer-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn(
            "count",
            response.data
        )

        self.assertIn(
            "results",
            response.data
        )

    def test_get_offers_contains_basic_fields(self):
        """
        Test that offers contain their basic response fields.
        """

        url = reverse("offer-list")

        response = self.client.get(url)

        offer = response.data["results"][0]

        self.assertIn(
            "id",
            offer
        )

        self.assertIn(
            "title",
            offer
        )

        self.assertIn(
            "description",
            offer
        )

        self.assertIn(
            "created_at",
            offer
        )

        self.assertIn(
            "updated_at",
            offer
        )

    def test_get_offers_contains_user(self):
        """
        Test that the offer response contains the business user ID.
        """

        url = reverse("offer-list")

        response = self.client.get(url)

        offer = response.data["results"][0]

        self.assertIn(
            "user",
            offer
        )

        self.assertEqual(
            offer["user"],
            self.business_user.id
        )

    def test_get_offers_contains_image(self):
        """
        Test that the offer response contains the image field.
        """

        url = reverse("offer-list")

        response = self.client.get(url)

        offer = response.data["results"][0]

        self.assertIn(
            "image",
            offer
        )

        self.assertIn(
            offer["image"],
            [None, ""]
        )

    def test_get_offers_contains_details(self):
        """
        Test that the offer response contains its associated details.
        """

        url = reverse("offer-list")

        response = self.client.get(url)

        offer = response.data["results"][0]

        self.assertIn(
            "details",
            offer
        )

        self.assertEqual(
            len(offer["details"]),
            1
        )

    def test_get_offers_contains_min_price(self):
        """
        Test that the response contains the minimum offer price.
        """

        url = reverse("offer-list")

        response = self.client.get(url)

        offer = response.data["results"][0]

        self.assertIn(
            "min_price",
            offer
        )

        self.assertEqual(
            float(offer["min_price"]),
            100.0
        )

    def test_get_offers_contains_min_delivery_time(self):
        """
        Test that the response contains the minimum delivery time.
        """

        url = reverse("offer-list")

        response = self.client.get(url)

        offer = response.data["results"][0]

        self.assertIn(
            "min_delivery_time",
            offer
        )

        self.assertEqual(
            offer["min_delivery_time"],
            7
        )

    def test_get_offers_contains_user_details(self):
        """
        Test that the response contains basic business user details.
        """

        url = reverse("offer-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            200
        )

        offer = response.data["results"][0]

        self.assertIn(
            "user_details",
            offer
        )

        self.assertIn(
            "first_name",
            offer["user_details"]
        )

        self.assertIn(
            "last_name",
            offer["user_details"]
        )

        self.assertIn(
            "username",
            offer["user_details"]
        )

    def test_get_offers_filters_by_creator_id(self):
        """
        Test that offers can be filtered by business user ID.
        """

        url = reverse("offer-list")

        response = self.client.get(
            url,
            {
                "creator_id": self.business_user.id
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        results = response.data["results"]

        self.assertEqual(
            len(results),
            1
        )

        self.assertEqual(
            results[0]["user"],
            self.business_user.id
        )

    def test_get_offers_filters_by_min_price(self):
        """
        Test that offers can be filtered by minimum price.
        """

        response = self.client.get(
            "/api/offers/",
            {
                "min_price": 200
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        results = response.data["results"]

        self.assertEqual(
            len(results),
            0
        )

    def test_get_offers_filters_by_max_delivery_time(self):
        """
        Test that offers can be filtered by maximum delivery time.
        """

        response = self.client.get(
            "/api/offers/",
            {
                "max_delivery_time": 5
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        results = response.data["results"]

        self.assertEqual(
            len(results),
            0
        )

    def test_get_offers_searches_title_and_description(self):
        """
        Test that offers can be searched by title or description.
        """

        response = self.client.get(
            "/api/offers/",
            {
                "search": "Website"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        results = response.data["results"]

        self.assertEqual(
            len(results),
            1
        )

        self.assertEqual(
            results[0]["title"],
            "Website Design"
        )

    def test_get_offers_orders_by_updated_at(self):
        """
        Test that offers can be ordered by their update timestamp.
        """

        older_offer = Offer.objects.create(
            business=self.business_user,
            title="Older Offer",
            description="Old",
        )

        newer_offer = Offer.objects.create(
            business=self.business_user,
            title="Newer Offer",
            description="New",
        )

        response = self.client.get(
            "/api/offers/",
            {
                "ordering": "-updated_at"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        results = response.data["results"]

        self.assertEqual(
            results[0]["id"],
            newer_offer.id
        )

    def test_get_offers_orders_by_min_price(self):
        """
        Test that offers can be ordered by their minimum price.
        """

        cheap_offer = Offer.objects.create(
            business=self.business_user,
            title="Cheap Website",
            description="Cheap",
        )

        expensive_offer = Offer.objects.create(
            business=self.business_user,
            title="Expensive Website",
            description="Expensive",
        )

        OfferDetail.objects.create(
            offer=cheap_offer,
            price=50,
            delivery_time_in_days=5
        )

        OfferDetail.objects.create(
            offer=expensive_offer,
            price=200,
            delivery_time_in_days=5
        )

        response = self.client.get(
            "/api/offers/",
            {
                "ordering": "min_price"
            }
        )

        results = response.data["results"]

        self.assertEqual(
            results[0]["id"],
            cheap_offer.id
        )

    def test_get_offers_default_ordering(self):
        """
        Test that offers use the default ordering when no ordering is specified.
        """

        response = self.client.get(
            "/api/offers/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        results = response.data["results"]

        self.assertEqual(
            results[0]["id"],
            self.offer.id
        )

    def test_get_offers_with_page_size(self):
        """
        Test that the page size can be customized using a query parameter.
        """

        response = self.client.get(
            "/api/offers/?page_size=2"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        results = response.data["results"]

        self.assertEqual(
            len(results),
            2
        )
