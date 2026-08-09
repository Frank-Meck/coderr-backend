from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from orders.models import Order


class CompletedOrderCountAPITest(APITestCase):
    """
    Test cases for the completed order count endpoint.

    These tests verify authentication requirements, correct order
    counting, and handling of non-existent business users.
    """

    def setUp(self):
        """
        Create the users and orders required for the test cases.

        Two completed orders and one in-progress order are created
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

        self.completed_order_1 = Order.objects.create(
            customer=self.customer,
            business=self.business,
            title="Completed Order 1",
            price=100,
            delivery_time_in_days=5,
            revisions=2,
            features=[
                "Feature"
            ],
            offer_type="basic",
            status="completed"
        )

        self.completed_order_2 = Order.objects.create(
            customer=self.customer,
            business=self.business,
            title="Completed Order 2",
            price=200,
            delivery_time_in_days=7,
            revisions=3,
            features=[
                "Feature"
            ],
            offer_type="basic",
            status="completed"
        )

        self.running_order = Order.objects.create(
            customer=self.customer,
            business=self.business,
            title="Running Order",
            price=150,
            delivery_time_in_days=5,
            revisions=1,
            features=[
                "Feature"
            ],
            offer_type="basic",
            status="in_progress"
        )

    def test_authenticated_user_can_get_completed_order_count(self):
        """
        Verify that an authenticated user can retrieve the
        completed order count for a business user.
        """
        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            f"/api/completed-order-count/{self.business.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["completed_order_count"],
            2
        )

    def test_unauthenticated_user_cannot_get_completed_order_count(self):
        """
        Verify that unauthenticated users cannot access the endpoint.
        """
        response = self.client.get(
            f"/api/completed-order-count/{self.business.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_business_user_not_found(self):
        """
        Verify that the endpoint returns 404 when the specified
        business user does not exist.
        """
        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.get(
            "/api/completed-order-count/9999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

