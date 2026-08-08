from django.test import TestCase

from users.models import User, Profile


class UserModelTest(TestCase):
    """
    Test the custom User and Profile models.

    Covers user creation, password hashing, user types,
    the User/Profile relationship, optional profile fields,
    and string representations.
    """

    def test_create_user(self):
        """
        Verify that a user can be created using the custom User model.

        The created user should contain the expected username,
        email, and account type. The password must also be usable
        for authentication.
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
        Verify the OneToOne relationship between User and Profile.

        A profile should be automatically created for a new user,
        and both sides of the relationship should reference the
        correct objects.
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
        Verify that optional profile fields use empty strings by default.

        Fields such as location, telephone number, and description
        should contain an empty string when no value is provided.
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
        Verify that a customer user can be created.

        The user's type should be stored as "customer".
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
        Verify that a business user can be created.

        The user's type should be stored as "business".
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
        Verify the string representation of a Profile.

        The string representation should contain the profile
        owner's first and last name.
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
