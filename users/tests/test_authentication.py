from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User, Profile


class AuthenticationTest(APITestCase):
    """
    Tests for authentication endpoints.

    Covers:
    - Registration
    - Login
    - Invalid authentication cases
    """

    def test_registration_success(self):
        """
        Happy path:
        User can register successfully.
        """

        response = self.client.post(
            "/api/registration/",
            {
                "username": "newcustomer",
                "email": "customer@test.de",
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

        self.assertEqual(
            response.data["username"],
            "newcustomer"
        )

        self.assertTrue(
            User.objects.filter(
                username="newcustomer"
            ).exists()
        )

    def test_registration_creates_profile(self):
        """
        Registration should create a profile
        through signals.py.
        """

        user = User.objects.create_user(
            username="signaluser",
            email="signal@test.de",
            password="password123",
            type="customer"
        )

        self.assertTrue(
            Profile.objects.filter(
                user=user
            ).exists()
        )

    def test_registration_password_mismatch(self):
        """
        Unhappy path:
        Password confirmation does not match.
        """

        response = self.client.post(
            "/api/registration/",
            {
                "username": "wrongpassword",
                "email": "wrong@test.de",
                "password": "password123",
                "repeated_password": "different123",
                "type": "customer"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_registration_duplicate_username(self):
        """
        Unhappy path:
        Username already exists.
        """

        User.objects.create_user(
            username="existinguser",
            password="password123",
            type="customer"
        )

        response = self.client.post(
            "/api/registration/",
            {
                "username": "existinguser",
                "email": "new@test.de",
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

    def test_login_success(self):
        """
        Happy path:
        Existing user can login.
        """

        User.objects.create_user(
            username="loginuser",
            password="password123",
            email="login@test.de",
            type="customer"
        )

        response = self.client.post(
            "/api/login/",
            {
                "username": "loginuser",
                "password": "password123"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn(
            "token",
            response.data
        )

        self.assertEqual(
            response.data["username"],
            "loginuser"
        )

    def test_login_wrong_password(self):
        """
        Unhappy path:
        Wrong password should fail.
        """

        User.objects.create_user(
            username="wronglogin",
            password="password123",
            type="customer"
        )

        response = self.client.post(
            "/api/login/",
            {
                "username": "wronglogin",
                "password": "wrongpassword"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_login_unknown_user(self):
        """
        Unhappy path:
        User does not exist.
        """

        response = self.client.post(
            "/api/login/",
            {
                "username": "doesnotexist",
                "password": "password123"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
