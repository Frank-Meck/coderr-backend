from django.test import TestCase
from users.models import User, Profile


class UserModelTest(TestCase):
    """
    Test suite for the custom User and Profile models.

    Verifies user creation, profile relationships, optional fields,
    user types, and string representations.
    """

    def test_create_user(self):
        """
        Test if a user can be created using the custom User model.

        Verifies:
        - username is stored correctly
        - user type is assigned correctly
        - password hashing works correctly
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
            user.type,
            "customer"
        )

        self.assertTrue(
            user.check_password("password123")
        )

    def test_user_profile_relation(self):
        """
        Test the OneToOne relationship between User and Profile.

        Verifies:
        - profile references the correct user
        - user can access the profile through related_name

        Relationship:
            User (1) -------- (1) Profile
        """

        user = User.objects.create_user(
            username="jane",
            password="password123",
            type="customer"
        )

        profile = Profile.objects.create(
            user=user,
            first_name="Jane",
            last_name="Doe"
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
        """
        Test that optional profile fields allow empty values.

        API requirement:
        Empty profile fields should return empty strings instead of NULL values.

        Verifies:
        - location
        - telephone number
        - description
        """

        user = User.objects.create_user(
            username="customer1",
            password="password123",
            type="customer"
        )

        profile = Profile.objects.create(
            user=user,
            first_name="",
            last_name=""
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
        """
        Test if business users can be created correctly.

        Verifies:
        - the user type field accepts the "business" choice
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
        Test the string representation of a Profile instance.

        Verifies:
        - __str__ returns the user's full name
        """

        user = User.objects.create_user(
            username="max",
            password="123456",
            type="business"
        )

        profile = Profile.objects.create(
            user=user,
            first_name="Max",
            last_name="Mustermann"
        )

        self.assertEqual(
            str(profile),
            "Max Mustermann"
        )
