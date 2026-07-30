from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User, Profile


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


class ProfileViewTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="profileuser",
            password="password123",
            type="customer"
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_get_profile(self):

        response = self.client.get(
            "/api/profile/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["username"],
            "profileuser"
        )

    def test_update_profile_data(self):

        profile = Profile.objects.get(
            user=self.user
        )

        profile.first_name = "Max"
        profile.last_name = "Mustermann"
        profile.save()

        response = self.client.get(
            "/api/profile/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["first_name"],
            "Max"
        )

        self.assertEqual(
            response.data["last_name"],
            "Mustermann"
        )

    def test_user_creation_creates_profile(self):

        user = User.objects.create_user(
            username="signaltest",
            password="password123",
            type="customer"
        )

        self.assertTrue(
            Profile.objects.filter(
                user=user
            ).exists()
        )
