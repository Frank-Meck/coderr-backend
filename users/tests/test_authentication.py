from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User, Profile


class AuthenticationTest(APITestCase):
    """
    Test the authentication-related API functionality.

    Covers successful registration, automatic profile creation,
    login, invalid registration data, and invalid login attempts.
    """

    def test_registration_success(self):
        """
        Verify that a user can register successfully.

        A valid registration request should return HTTP 201,
        return the registered username, and create the user
        in the database.
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
        Verify that creating a user also creates a profile.

        The User post_save signal should automatically create
        a corresponding Profile instance for the new user.
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
        Verify that registration fails when passwords do not match.

        A registration request with different password and
        repeated_password values should return HTTP 400.
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
        Verify that registration fails for an existing username.

        A username that is already registered should not be
        accepted again and should return HTTP 400.
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
        Verify that an existing user can log in successfully.

        Valid login credentials should return HTTP 200 and
        an authentication token together with the username.
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
        Verify that login fails when the password is incorrect.

        An existing user submitting an incorrect password should
        receive HTTP 400.
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
        Verify that login fails when the username does not exist.

        Authentication with an unknown username should return
        HTTP 400.
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
