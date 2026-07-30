from django.test import TestCase
from users.models import User, Profile


class UserModelTest(TestCase):
    """
    Test suite for the custom User and Profile models.

    Verifies user creation, profile relationships, optional fields,
    user types, and string representations.
    """

    def test_create_user(self):

        user = User.objects.create_user(
            username="testuser",
            email="test@test.de",
            password="password123",
            type="customer"
        )

        self.assertEqual(
            user.username,
            "testuser"
        )

        self.assertEqual(
            user.type,
            "customer"
        )

        self.assertTrue(
            user.check_password("password123")
        )

    def test_user_profile_relation(self):

        user = User.objects.create_user(
            username="jane",
            password="password123",
            type="customer"
        )

        profile = Profile.objects.get(
            user=user
        )

        self.assertEqual(
            profile.user,
            user
        )

        self.assertEqual(
            user.profile,
            profile
        )

    def test_profile_optional_fields(self):

        user = User.objects.create_user(
            username="customer1",
            password="password123",
            type="customer"
        )

        profile = Profile.objects.get(
            user=user
        )

        self.assertEqual(
            profile.location,
            ""
        )

        self.assertEqual(
            profile.tel,
            ""
        )

        self.assertEqual(
            profile.description,
            ""
        )

    def test_user_type_choices(self):

        user = User.objects.create_user(
            username="business",
            password="password123",
            type="business"
        )

        self.assertEqual(
            user.type,
            "business"
        )

    def test_profile_str(self):

        user = User.objects.create_user(
            username="max",
            password="123456",
            type="business"
        )

        profile = Profile.objects.get(
            user=user
        )

        profile.first_name = "Max"
        profile.last_name = "Mustermann"
        profile.save()

        self.assertEqual(
            str(profile),
            "Max Mustermann"
        )
