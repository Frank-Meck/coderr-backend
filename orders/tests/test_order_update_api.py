from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from orders.models import Order


class OrderUpdateAPITest(APITestCase):
    """
    Test cases for updating orders.

    These tests verify that only the business user associated with
    an order can update it and that invalid requests are rejected.
    """

    def setUp(self):
        """
        Create the users and order required for the test cases.

        One customer and two business users are created. The order
        belongs to the first business user.
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

        self.other_business = User.objects.create_user(
            username="other_business@test.com",
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

    def test_business_can_update_order_status(self):
        """
        Verify that the business user associated with the order
        can update its status.
        """
        self.client.force_authenticate(
            user=self.business
        )

        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {
                "status": "completed"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            "completed"
        )

    def test_unauthenticated_user_cannot_update_order(self):
        """
        Verify that unauthenticated users cannot update an order.
        """
        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {
                "status": "completed"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_customer_cannot_update_order(self):
        """
        Verify that customers cannot update an order.
        """
        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {
                "status": "completed"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_other_business_cannot_update_foreign_order(self):
        """
        Verify that a different business user cannot update
        an order that does not belong to them.
        """
        self.client.force_authenticate(
            user=self.other_business
        )

        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {
                "status": "completed"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_invalid_status_cannot_update_order(self):
        """
        Verify that an order cannot be updated with an invalid status.
        """
        self.client.force_authenticate(
            user=self.business
        )

        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {
                "status": "invalid_status"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_order_not_found(self):
        """
        Verify that updating a non-existent order returns
        a 404 response.
        """
        self.client.force_authenticate(
            user=self.business
        )

        response = self.client.patch(
            "/api/orders/999/",
            {
                "status": "completed"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
