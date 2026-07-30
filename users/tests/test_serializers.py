from django.test import TestCase

from users.api.serializers import RegistrationSerializer


class RegistrationSerializerTest(TestCase):

    def test_valid_registration_data(self):

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

    def test_registration_serializer_valid(self):

        data = {
            "username": "newuser",
            "email": "test@test.de",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer"
        }

        serializer = RegistrationSerializer(data=data)

        is_valid = serializer.is_valid()

        self.assertTrue(is_valid)

    def test_username_required(self):

        data = {
            "email": "test@test.de",
            "password": "password123"
        }

        serializer = RegistrationSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

    def test_registration_serializer_create_user(self):

        data = {
            "username": "newuser",
            "email": "new@test.de",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer"
        }

        serializer = RegistrationSerializer(data=data)

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

        self.assertTrue(
            user.check_password("password123")
        )
