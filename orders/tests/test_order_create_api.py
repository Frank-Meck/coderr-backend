from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from offers.models import Offer, OfferDetail
from orders.models import Order


class OrderCreateAPITest(APITestCase):
    """
    Test cases for creating orders.

    These tests verify that customers can create orders from offer
    details and that invalid users or input data are rejected.
    """

    def setUp(self):
        """
        Create the users, offer, and offer detail required for the tests.
        """
        self.customer = User.objects.create_user(
            username="customer@test.com",
            password="test123",
            type="customer"
        )

        self.business = User.objects.create_user(
            username="business@test.com",
            password="test123",
            type="business"
        )

        self.offer = Offer.objects.create(
            business=self.business,
            title="Logo Design",
            description="Design"
        )

        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic",
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=[
                "Logo Design",
                "Visitenkarten"
            ],
            offer_type="basic"
        )

    def test_customer_can_create_order(self):
        """
        Verify that an authenticated customer can create an order
        from an existing offer detail.

        The created order must contain the customer, business,
        offer detail, and all relevant offer detail information.
        """
        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.post(
            "/api/orders/",
            {
                "offer_detail_id": self.offer_detail.id
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Order.objects.count(),
            1
        )

        order = Order.objects.first()

        self.assertEqual(
            order.customer,
            self.customer
        )

        self.assertEqual(
            order.business,
            self.business
        )

        self.assertEqual(
            order.offer_detail,
            self.offer_detail
        )

        self.assertEqual(
            order.title,
            self.offer_detail.title
        )

        self.assertEqual(
            order.revisions,
            self.offer_detail.revisions
        )

        self.assertEqual(
            order.delivery_time_in_days,
            self.offer_detail.delivery_time_in_days
        )

        self.assertEqual(
            order.price,
            self.offer_detail.price
        )

        self.assertEqual(
            order.features,
            self.offer_detail.features
        )

        self.assertEqual(
            order.offer_type,
            self.offer_detail.offer_type
        )

    def test_unauthenticated_user_cannot_create_order(self):
        """
        Verify that unauthenticated users cannot create an order.
        """
        response = self.client.post(
            "/api/orders/",
            {
                "offer_detail_id": self.offer_detail.id
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_business_cannot_create_order(self):
        """
        Verify that business users are not allowed to create orders.
        """
        self.client.force_authenticate(
            user=self.business
        )

        response = self.client.post(
            "/api/orders/",
            {
                "offer_detail_id": self.offer_detail.id
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_offer_detail_id_is_required(self):
        """
        Verify that the offer detail ID is required when creating
        an order.
        """
        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.post(
            "/api/orders/",
            {},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_offer_detail_not_found(self):
        """
        Verify that a 404 response is returned when the specified
        offer detail does not exist.
        """
        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.post(
            "/api/orders/",
            {
                "offer_detail_id": 99999
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

