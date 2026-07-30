from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class RegistrationViewTest(APITestCase):

    def test_user_registration(self):

        response = self.client.post(
            "/api/registration/",
            {
                "username": "testuser",
                "email": "test@test.de",
                "password": "password123",
                "repeated_password": "password123",
                "type": "customer"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            User.objects.filter(
                username="testuser"
            ).exists()
        )


    def test_registration_invalid_password_confirmation(self):

        response = self.client.post(
            "/api/registration/",
            {
                "username": "testuser",
                "email": "test@test.de",
                "password": "password123",
                "repeated_password": "wrongpassword",
                "type": "customer"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


    def test_registration_duplicate_username(self):

        User.objects.create_user(
            username="testuser",
            email="test@test.de",
            password="password123",
            type="customer"
        )


        response = self.client.post(
            "/api/registration/",
            {
                "username": "testuser",
                "email": "another@test.de",
                "password": "password123",
                "repeated_password": "password123",
                "type": "customer"
            },
            format="json"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )