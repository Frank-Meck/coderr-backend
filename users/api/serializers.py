from rest_framework import serializers

from users.models import User, Profile


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.

    Validates the registration data, including the repeated password,
    and creates a new User instance with a securely hashed password.
    """

    repeated_password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password",
            "repeated_password",
            "type",
        ]

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, attrs):
        """
        Validate that both submitted passwords are identical.

        Args:
            attrs: Validated registration data.

        Returns:
            dict: Validated registration data.

        Raises:
            serializers.ValidationError: If the passwords do not match.
        """
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                "Passwords do not match"
            )

        return attrs

    def create(self, validated_data):
        """
        Create a new user from validated registration data.

        The repeated password is removed before the User instance
        is created. Django's create_user method is used to ensure
        that the password is stored securely as a hash.

        Args:
            validated_data: Validated registration data.

        Returns:
            User: The newly created user instance.
        """
        validated_data.pop(
            "repeated_password"
        )

        return User.objects.create_user(
            **validated_data
        )


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for reading and updating user profile information.

    Provides profile data together with selected read-only information
    from the associated User instance, including username and user type.
    The user's email address can also be updated through the profile.
    """

    user = serializers.IntegerField(
        source="user.id",
        read_only=True
    )

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email"
    )

    type = serializers.CharField(
        source="user.type",
        read_only=True
    )

    class Meta:
        model = Profile

        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]

        read_only_fields = [
            "user",
            "username",
            "type",
            "created_at",
        ]

    def update(self, instance, validated_data):
        """
        Update profile data and the associated user's email address.

        Profile fields are updated through the Profile instance.
        The email address belongs to the related User instance and
        is therefore handled separately before the profile is updated.

        Args:
            instance: The existing Profile instance.
            validated_data: Validated profile data.

        Returns:
            Profile: The updated profile instance.
        """
        user_data = validated_data.pop(
            "user",
            {}
        )

        email = user_data.get(
            "email"
        )

        if email:
            instance.user.email = email
            instance.user.save()

        return super().update(
            instance,
            validated_data
        )
