from django.test import TestCase

from users.models import User, Profile


class UserModelTest(TestCase):
    """
    Test suite for the custom User and Profile models.

    Verifies:
    - user creation
    - password hashing
    - user types
    - profile relationship
    - profile optional fields
    - string representation
    """

    def test_create_user(self):
        """
        Test if a user can be created using the custom User model.
        """

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
            user.email,
            "test@test.de"
        )

        self.assertEqual(
            user.type,
            "customer"
        )

        self.assertTrue(
            user.check_password(
                "password123"
            )
        )

    def test_user_profile_relation(self):
        """
        Test the OneToOne relationship between User and Profile.
        """

        user = User.objects.create_user(
            username="jane",
            password="password123",
            type="customer"
        )

        profile = user.profile

        profile.first_name = "Jane"
        profile.last_name = "Doe"
        profile.save()

        self.assertEqual(
            profile.user,
            user
        )

        self.assertEqual(
            user.profile,
            profile
        )

    def test_profile_optional_fields(self):
        """
        Test that optional profile fields allow empty values.
        """

        user = User.objects.create_user(
            username="customer1",
            password="password123",
            type="customer"
        )

        profile = user.profile

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

    def test_user_type_customer(self):
        """
        Test customer user type.
        """

        user = User.objects.create_user(
            username="customer",
            password="password123",
            type="customer"
        )

        self.assertEqual(
            user.type,
            "customer"
        )

    def test_user_type_business(self):
        """
        Test business user type.
        """

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
        """
        Test the string representation of Profile.
        """

        user = User.objects.create_user(
            username="max",
            password="123456",
            type="business"
        )

        profile = user.profile

        profile.first_name = "Max"
        profile.last_name = "Mustermann"
        profile.save()

        self.assertEqual(
            str(profile),
            "Max Mustermann"
        )
