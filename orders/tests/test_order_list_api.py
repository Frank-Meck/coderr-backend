from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from orders.models import Order


class OrderListAPITest(APITestCase):

    def setUp(self):

        self.customer = User.objects.create_user(
            username="customer@test.com",
            password="test123",
            type="customer"
        )

        self.other_customer = User.objects.create_user(
            username="other_customer@test.com",
            password="test123",
            type="customer"
        )

        self.business = User.objects.create_user(
            username="business@test.com",
            password="test123",
            type="business"
        )

        self.order = Order.objects.create(
            customer=self.customer,
            business=self.business,
            title="Logo Design",
            price=150,
            delivery_time_in_days=5,
            revisions=3,
            features=[
                "Logo Design",
                "Visitenkarten"
            ],
            offer_type="basic",
            status="in_progress"
        )

        self.foreign_order = Order.objects.create(
            customer=self.other_customer,
            business=self.business,
            title="Foreign Order",
            price=200,
            delivery_time_in_days=7,
            revisions=1,
            features=[
                "Something"
            ],
            offer_type="basic",
            status="in_progress"
        )

    def test_customer_can_see_own_orders(self):

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            "/api/orders/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["title"],
            "Logo Design"
        )

    def test_unauthenticated_user_cannot_get_orders(self):

        response = self.client.get(
            "/api/orders/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_customer_cannot_see_foreign_orders(self):

        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            "/api/orders/"
        )

        order_ids = [
            order["id"]
            for order in response.data
        ]

        self.assertNotIn(
            self.foreign_order.id,
            order_ids
        )


    def test_business_can_see_own_orders(self):

        self.client.force_authenticate(
            user=self.business
        )

        response = self.client.get(
            "/api/orders/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            2
        )