"""
Tests for the offers API models.

Tests the creation, relationships, default values, timestamps,
string representations, and database constraints of offers
and offer details.
"""

from django.test import TestCase
from django.db import IntegrityError

from users.models import User
from offers.models import Offer, OfferDetail


class OfferModelTest(TestCase):
    """
    Test the Offer model.
    """

    def setUp(self):
        """
        Create a business user for the offer tests.
        """

        self.business_user = User.objects.create_user(
            username="business_user",
            password="testpass123",
            type="business"
        )

    def test_create_offer(self):
        """
        Test that an offer can be created with a business user.
        """

        offer = Offer.objects.create(
            business=self.business_user,
            title="Website Design",
            description="Professionelles Webdesign"
        )

        self.assertEqual(
            offer.title,
            "Website Design"
        )

        self.assertEqual(
            offer.business,
            self.business_user
        )

    def test_offer_string_representation(self):
        """
        Test the string representation of an offer.
        """

        offer = Offer.objects.create(
            business=self.business_user,
            title="Logo Design"
        )

        self.assertEqual(
            str(offer),
            "Logo Design"
        )

    def test_offer_optional_fields(self):
        """
        Test the default values of optional offer fields.
        """

        offer = Offer.objects.create(
            business=self.business_user,
            title="SEO Angebot"
        )

        self.assertEqual(
            offer.description,
            ""
        )

        self.assertFalse(
            offer.image
        )

    def test_offer_timestamps_are_created(self):
        """
        Test that creation and update timestamps are set automatically.
        """

        offer = Offer.objects.create(
            business=self.business_user,
            title="Web App"
        )

        self.assertIsNotNone(
            offer.created_at
        )

        self.assertIsNotNone(
            offer.updated_at
        )


class OfferDetailModelTest(TestCase):
    """
    Test the OfferDetail model.
    """

    def setUp(self):
        """
        Create a business user and an offer for the detail tests.
        """

        self.business_user = User.objects.create_user(
            username="business_user",
            password="testpass123",
            type="business"
        )

        self.offer = Offer.objects.create(
            business=self.business_user,
            title="Website Design"
        )

    def test_create_offer_detail(self):
        """
        Test that an offer detail can be created successfully.
        """

        detail = OfferDetail.objects.create(
            offer=self.offer,
            offer_type="basic",
            title="Basic Paket",
            price=100,
            delivery_time_in_days=7
        )

        self.assertEqual(
            detail.offer,
            self.offer
        )

        self.assertEqual(
            detail.price,
            100
        )

        self.assertEqual(
            detail.delivery_time_in_days,
            7
        )

    def test_offer_has_multiple_details(self):
        """
        Test that an offer can have multiple details with different types.
        """

        OfferDetail.objects.create(
            offer=self.offer,
            offer_type="basic",
            title="Basic",
            price=100,
            delivery_time_in_days=7
        )

        OfferDetail.objects.create(
            offer=self.offer,
            offer_type="premium",
            title="Premium",
            price=300,
            delivery_time_in_days=14
        )

        self.assertEqual(
            self.offer.details.count(),
            2
        )

    def test_offer_detail_default_values(self):
        """
        Test the default values of revisions and features.
        """

        detail = OfferDetail.objects.create(
            offer=self.offer,
            offer_type="standard",
            title="Standard",
            price=200,
            delivery_time_in_days=10
        )

        self.assertEqual(
            detail.revisions,
            0
        )

        self.assertEqual(
            detail.features,
            {}
        )

    def test_offer_detail_unique_offer_type_constraint(self):
        """
        Test that an offer cannot have duplicate detail types.
        """

        OfferDetail.objects.create(
            offer=self.offer,
            offer_type="basic",
            title="Basic",
            price=100,
            delivery_time_in_days=7
        )

        with self.assertRaises(IntegrityError):

            OfferDetail.objects.create(
                offer=self.offer,
                offer_type="basic",
                title="Basic nochmal",
                price=150,
                delivery_time_in_days=10
            )

    def test_offer_detail_string_representation(self):
        """
        Test the string representation of an offer detail.
        """

        detail = OfferDetail.objects.create(
            offer=self.offer,
            offer_type="premium",
            title="Premium Paket",
            price=300,
            delivery_time_in_days=14
        )

        self.assertEqual(
            str(detail),
            "Website Design - premium"
        )

