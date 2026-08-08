from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class LoginViewTest(APITestCase):
    """
    Test the login endpoint.

    Covers successful authentication, invalid credentials,
    unknown users, and missing login fields.
    """

    def setUp(self):
        """
        Create a test user before each test.

        The user is created with a known password so that
        successful and unsuccessful authentication attempts
        can be tested.
        """
        self.user = User.objects.create_user(
            username="loginuser",
            email="login@test.de",
            password="password123",
            type="customer"
        )

    def test_login_success(self):
        """
        Verify successful user authentication.

        A valid username and password should return HTTP 200
        together with an authentication token and user information.
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
        Verify that authentication fails with an incorrect password.

        An existing user submitting the wrong password should receive
        HTTP 400 and no successful authentication response.
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
        Verify that authentication fails for an unknown username.

        A username that does not exist should result in HTTP 400.
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
        Verify that login fails when the username is missing.

        The login endpoint requires both username and password,
        therefore a request without username should return HTTP 400.
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
        Verify that login fails when the password is missing.

        The login endpoint requires both username and password,
        therefore a request without password should return HTTP 400.
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
