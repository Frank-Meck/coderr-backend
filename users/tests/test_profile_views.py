from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class ProfileDetailViewTest(APITestCase):
    """
    Tests for GET and PATCH /api/profile/{pk}/
    """

    def setUp(self):

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
        User can update email.
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
        Authenticated user can retrieve profile.
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
        Anonymous user cannot retrieve profile.
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
        User can update own profile.
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
        User cannot update another profile.
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
    Tests for business and customer profile lists.
    """

    def setUp(self):

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
        Returns only business profiles.
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
        Returns only customer profiles.
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
