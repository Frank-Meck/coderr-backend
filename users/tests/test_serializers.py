from django.test import TestCase

from users.api.serializers import RegistrationSerializer
from users.models import User


class RegistrationSerializerTest(TestCase):
    """
    Test the RegistrationSerializer.

    Covers validation of registration data, password confirmation,
    required fields, duplicate usernames, user creation, and
    secure password storage.
    """

    def test_valid_registration_data(self):
        """
        Verify that valid registration data passes validation.

        A valid username, email, password, repeated password, and
        user type should result in a valid serializer.
        """
        data = {
            "username": "testuser",
            "email": "test@test.de",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer",
        }

        serializer = RegistrationSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid()
        )

    def test_password_confirmation_mismatch(self):
        """
        Verify that registration fails when passwords do not match.

        The serializer should return a validation error when
        password and repeated_password contain different values.
        """
        data = {
            "username": "testuser",
            "email": "test@test.de",
            "password": "password123",
            "repeated_password": "wrongpassword",
            "type": "customer",
        }

        serializer = RegistrationSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "Passwords do not match",
            str(serializer.errors)
        )

    def test_username_required(self):
        """
        Verify that username is a required registration field.

        The serializer should reject registration data when
        no username is provided.
        """
        data = {
            "email": "test@test.de",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer",
        }

        serializer = RegistrationSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "username",
            serializer.errors
        )

    def test_duplicate_username(self):
        """
        Verify that duplicate usernames are rejected.

        Registration data containing a username that already exists
        should fail serializer validation.
        """
        User.objects.create_user(
            username="existinguser",
            email="old@test.de",
            password="password123",
            type="customer"
        )

        data = {
            "username": "existinguser",
            "email": "new@test.de",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer",
        }

        serializer = RegistrationSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "username",
            serializer.errors
        )

    def test_create_user_successfully(self):
        """
        Verify that the serializer creates a user correctly.

        The created user should contain the expected username,
        email, and account type, and the supplied password should
        be usable for authentication.
        """
        data = {
            "username": "newuser",
            "email": "new@test.de",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer",
        }

        serializer = RegistrationSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid()
        )

        user = serializer.save()

        self.assertEqual(
            user.username,
            "newuser"
        )

        self.assertEqual(
            user.email,
            "new@test.de"
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

    def test_password_is_not_saved_plain_text(self):
        """
        Verify that the user's password is stored as a hash.

        The password stored in the database must not be equal to
        the plain-text password supplied during registration.
        """
        data = {
            "username": "secureuser",
            "email": "secure@test.de",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer",
        }

        serializer = RegistrationSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid()
        )

        user = serializer.save()

        self.assertNotEqual(
            user.password,
            "password123"
        )
