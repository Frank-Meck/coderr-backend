from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User, Profile


class RegistrationViewTest(APITestCase):
    """
    Test the user registration endpoint.

    Covers successful registration and validation errors such as
    password mismatches and duplicate usernames.
    """

    def test_user_registration_success(self):
        """
        Verify that a user can register successfully.

        A valid registration request should return HTTP 201 and
        create a corresponding User instance in the database.
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
        Verify that registration fails when passwords do not match.

        A password confirmation mismatch should return HTTP 400.
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
        Verify that registration fails for an existing username.

        A duplicate username should return HTTP 400.
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
    Test the individual user profile endpoint.

    Covers authenticated profile retrieval and automatic profile
    creation after user registration.
    """

    def setUp(self):
        """
        Create an authenticated test user and its profile.

        The authentication is applied to the test client so that
        protected profile endpoints can be tested.
        """
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
        Verify that an authenticated user can retrieve a profile.

        The response should return HTTP 200 and contain the expected
        username and profile information.
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
        Verify that a profile is automatically created for a new user.

        The User post-save signal should create a corresponding
        Profile instance.
        """
        self.assertTrue(
            Profile.objects.filter(
                user=self.user
            ).exists()
        )


class LoginViewTest(APITestCase):
    """
    Test the user login endpoint.

    Covers successful authentication as well as invalid credentials.
    """

    def setUp(self):
        """
        Create a user with known login credentials for the tests.
        """
        self.user = User.objects.create_user(
            username="loginuser",
            email="login@test.de",
            password="password123",
            type="customer"
        )

    def test_login_success(self):
        """
        Verify that a user can log in with valid credentials.

        A successful login should return HTTP 200 and an authentication
        token.
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
        Verify that login fails when the password is incorrect.

        Invalid credentials should return HTTP 400.
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
        Verify that login fails when the username does not exist.

        Invalid credentials should return HTTP 400.
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