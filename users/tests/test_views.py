from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User, Profile


class RegistrationViewTest(APITestCase):
    """
    Tests for POST /api/registration/
    """

    def test_user_registration_success(self):
        """
        Happy path:
        User can register successfully.
        """

        response = self.client.post(
            "/api/registration/",
            {
                "username": "newuser",
                "email": "new@test.de",
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
                username="newuser"
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
                "username": "wrongpassworduser",
                "email": "wrong@test.de",
                "password": "password123",
                "repeated_password": "wrong123",
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
            email="old@test.de",
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


class ProfileViewTest(APITestCase):
    """
    Tests for GET /api/profile/
    """

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
        """
        Happy path:
        Authenticated user can get profile.
        """

        profile = self.user.profile

        profile.first_name = "Max"
        profile.last_name = "Mustermann"
        profile.save()

        response = self.client.get(
            f"/api/profile/{self.user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["username"],
            "profileuser"
        )

        self.assertEqual(
            response.data["first_name"],
            "Max"
        )

    def test_profile_created_by_signal(self):
        """
        Test that a profile exists after user creation.
        """

        self.assertTrue(
            Profile.objects.filter(
                user=self.user
            ).exists()
        )


class LoginViewTest(APITestCase):
    """
    Tests for POST /api/login/
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username="loginuser",
            email="login@test.de",
            password="password123",
            type="customer"
        )

    def test_login_success(self):
        """
        Happy path:
        User can login with correct credentials.
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

    def test_login_wrong_password(self):
        """
        Unhappy path:
        Wrong password.
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

    def test_login_unknown_user(self):
        """
        Unhappy path:
        Username does not exist.
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
