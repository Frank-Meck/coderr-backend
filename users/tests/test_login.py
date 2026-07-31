from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class LoginViewTest(APITestCase):
    """
    Tests for POST /api/login/

    Covers:
    - successful login
    - wrong password
    - unknown user
    - missing fields
    """

    def setUp(self):
        """
        Create test user before each test.
        """

        self.user = User.objects.create_user(
            username="loginuser",
            email="login@test.de",
            password="password123",
            type="customer"
        )

    def test_login_success(self):
        """
        Happy Path:

        User logs in with correct credentials.
        Expected:
        - HTTP 200
        - Token returned
        - User information returned
        """

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

        self.assertEqual(
            response.data["email"],
            "login@test.de"
        )

        self.assertIn(
            "user_id",
            response.data
        )

    def test_login_wrong_password(self):
        """
        Unhappy Path:

        Existing user but wrong password.

        Expected:
        HTTP 400
        """

        response = self.client.post(
            "/api/login/",
            {
                "username": "loginuser",
                "password": "wrongpassword"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_login_unknown_username(self):
        """
        Unhappy Path:

        Username does not exist.

        Expected:
        HTTP 400
        """

        response = self.client.post(
            "/api/login/",
            {
                "username": "unknownuser",
                "password": "password123"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_login_missing_username(self):
        """
        Unhappy Path:

        Username missing.

        Expected:
        HTTP 400
        """

        response = self.client.post(
            "/api/login/",
            {
                "password": "password123"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_login_missing_password(self):
        """
        Unhappy Path:

        Password missing.

        Expected:
        HTTP 400
        """

        response = self.client.post(
            "/api/login/",
            {
                "username": "loginuser"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
