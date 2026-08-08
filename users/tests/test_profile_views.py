from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class ProfileDetailViewTest(APITestCase):
    """
    Test the individual profile endpoint.

    Covers profile retrieval, profile updates, authentication,
    and ownership permissions for GET and PATCH requests.
    """

    def setUp(self):
        """
        Create and authenticate a test customer.

        The created user is used as the owner of the profile
        throughout the individual profile tests.
        """
        self.user = User.objects.create_user(
            username="profileuser",
            email="profile@test.de",
            password="password123",
            type="customer"
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_update_email(self):
        """
        Verify that a user can update their email address.

        A valid PATCH request should return HTTP 200 and update
        the email address of the associated User instance.
        """
        response = self.client.patch(
            f"/api/profile/{self.user.id}/",
            {
                "email": "newmail@test.de"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.email,
            "newmail@test.de"
        )

    def test_get_profile_authenticated(self):
        """
        Verify that an authenticated user can retrieve a profile.

        The endpoint should return HTTP 200 and the expected
        profile information.
        """
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

    def test_get_profile_unauthenticated(self):
        """
        Verify that unauthenticated users cannot retrieve profiles.

        Accessing the protected endpoint without authentication
        should return HTTP 401.
        """
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            f"/api/profile/{self.user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_update_own_profile(self):
        """
        Verify that a user can update their own profile.

        A valid PATCH request to the user's own profile should
        return HTTP 200 and update the submitted profile fields.
        """
        response = self.client.patch(
            f"/api/profile/{self.user.id}/",
            {
                "first_name": "Max",
                "last_name": "Mustermann"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["first_name"],
            "Max"
        )

    def test_update_other_profile_forbidden(self):
        """
        Verify that a user cannot update another user's profile.

        Attempting to modify a profile owned by another user
        should return HTTP 403.
        """
        other_user = User.objects.create_user(
            username="otheruser",
            password="password123",
            type="customer"
        )

        response = self.client.patch(
            f"/api/profile/{other_user.id}/",
            {
                "first_name": "Forbidden"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )


class ProfileListViewTest(APITestCase):
    """
    Test the business and customer profile list endpoints.

    Verifies that the endpoints return profiles belonging only
    to the requested user type and that authenticated users can
    view profiles of other users.
    """

    def setUp(self):
        """
        Create business and customer test users.

        The customer user is authenticated and used to access
        the protected profile list endpoints.
        """
        self.business_user = User.objects.create_user(
            username="businessuser",
            password="password123",
            type="business"
        )

        self.customer_user = User.objects.create_user(
            username="customeruser",
            password="password123",
            type="customer"
        )

        self.client.force_authenticate(
            user=self.customer_user
        )

    def test_get_business_profiles(self):
        """
        Verify that the business profile endpoint returns only
        business users.

        The response should contain the business user and exclude
        the customer user.
        """
        response = self.client.get(
            "/api/profiles/business/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        usernames = [
            profile["username"]
            for profile in response.data
        ]

        self.assertIn(
            "businessuser",
            usernames
        )

        self.assertNotIn(
            "customeruser",
            usernames
        )

    def test_get_customer_profiles(self):
        """
        Verify that the customer profile endpoint returns only
        customer users.

        The response should contain the customer user.
        """
        response = self.client.get(
            "/api/profiles/customer/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        usernames = [
            profile["username"]
            for profile in response.data
        ]

        self.assertIn(
            "customeruser",
            usernames
        )

    def test_get_foreign_profile_allowed(self):
        """
        Verify that authenticated users can view other profiles.

        An authenticated user should be able to retrieve another
        user's profile and receive HTTP 200.
        """
        foreign_user = User.objects.create_user(
            username="foreign",
            password="password123",
            type="business"
        )

        response = self.client.get(
            f"/api/profile/{foreign_user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )