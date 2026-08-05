from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from offers.models import Offer, OfferDetail
from orders.models import Order


class OrderCreateAPITest(APITestCase):

    def setUp(self):

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

        print(response.data)

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