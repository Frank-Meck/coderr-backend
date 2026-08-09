from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from orders.models import Order


class OrderCountAPITest(APITestCase):
    """
    Test cases for the order count endpoint.

    These tests verify authentication requirements, correct counting
    of in-progress orders, and handling of invalid user IDs.
    """

    def setUp(self):
        """
        Create the users and orders required for the test cases.

        Two in-progress orders and one completed order are created
        for the same business user.
        """
        self.business = User.objects.create_user(
            username="business@test.com",
            password="test123",
            type="business"
        )

        self.customer = User.objects.create_user(
            username="customer@test.com",
            password="test123",
            type="customer"
        )

        self.order_one = Order.objects.create(
            customer=self.customer,
            business=self.business,
            title="Logo Design",
            price=150,
            delivery_time_in_days=5,
            revisions=3,
            features=[
                "Logo"
            ],
            offer_type="basic",
            status="in_progress"
        )

        self.order_two = Order.objects.create(
            customer=self.customer,
            business=self.business,
            title="Website",
            price=500,
            delivery_time_in_days=10,
            revisions=2,
            features=[
                "Frontend"
            ],
            offer_type="premium",
            status="in_progress"
        )

        self.completed_order = Order.objects.create(
            customer=self.customer,
            business=self.business,
            title="Completed Order",
            price=100,
            delivery_time_in_days=3,
            revisions=1,
            features=[
                "Done"
            ],
            offer_type="basic",
            status="completed"
        )

    def test_authenticated_user_can_get_business_order_count(self):
        """
        Verify that an authenticated user can retrieve the number
        of in-progress orders for a business user.
        """
        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            f"/api/order-count/{self.business.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["order_count"],
            2
        )

    def test_unauthenticated_user_cannot_get_order_count(self):
        """
        Verify that unauthenticated users cannot access the endpoint.
        """
        response = self.client.get(
            f"/api/order-count/{self.business.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_order_count_business_user_not_found(self):
        """
        Verify that the endpoint returns 404 when the specified
        business user does not exist.
        """
        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            "/api/order-count/9999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_customer_id_returns_not_found(self):
        """
        Verify that a customer user ID cannot be used as a
        business user ID.
        """
        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            f"/api/order-count/{self.customer.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

