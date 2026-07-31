from django.test import TestCase

from users.api.serializers import RegistrationSerializer
from users.models import User


class RegistrationSerializerTest(TestCase):
    """
    Tests for the RegistrationSerializer.

    Covers:
    - valid registration data
    - validation errors
    - duplicate users
    - user creation
    """

    def test_valid_registration_data(self):
        """
        Test that valid registration data passes validation.
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
        Test that registration fails if passwords do not match.
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
        Test that username is required.
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
        Test that duplicate usernames are rejected.
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
        Test that serializer creates a user correctly.
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
        Test that passwords are hashed.
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
