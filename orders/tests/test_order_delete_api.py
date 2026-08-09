from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from orders.models import Order


class OrderDeleteAPITest(APITestCase):
    """
    Test cases for deleting orders.

    These tests verify that only admin users can delete orders
    and that unauthorized or invalid requests are rejected.
    """

    def setUp(self):
        """
        Create the users and order required for the test cases.
        """
        self.admin = User.objects.create_user(
            username="admin@test.com",
            password="test123",
            is_staff=True
        )

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

        self.order = Order.objects.create(
            customer=self.customer,
            business=self.business,
            title="Logo Design",
            price=150,
            delivery_time_in_days=5,
            revisions=3,
            features=[
                "Logo Design"
            ],
            offer_type="basic",
            status="in_progress"
        )

    def test_admin_can_delete_order(self):
        """
        Verify that an authenticated admin user can delete an order.
        """
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.delete(
            f"/api/orders/{self.order.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Order.objects.count(),
            0
        )

    def test_customer_cannot_delete_order(self):
        """
        Verify that a customer cannot delete an order.
        """
        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.delete(
            f"/api/orders/{self.order.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            Order.objects.count(),
            1
        )

    def test_unauthenticated_user_cannot_delete_order(self):
        """
        Verify that unauthenticated users cannot delete an order.
        """
        response = self.client.delete(
            f"/api/orders/{self.order.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_delete_non_existing_order(self):
        """
        Verify that deleting a non-existent order returns a 404 response.
        """
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.delete(
            "/api/orders/9999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

