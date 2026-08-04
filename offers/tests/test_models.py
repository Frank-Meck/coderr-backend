from django.test import TestCase
from django.db import IntegrityError

from users.models import User
from offers.models import Offer, OfferDetail


class OfferModelTest(TestCase):

    def setUp(self):

        self.business_user = User.objects.create_user(
            username="business_user",
            password="testpass123",
            type="business"
        )

    def test_create_offer(self):

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

        offer = Offer.objects.create(
            business=self.business_user,
            title="Logo Design"
        )

        self.assertEqual(
            str(offer),
            "Logo Design"
        )

    def test_offer_optional_fields(self):

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

    def setUp(self):

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
