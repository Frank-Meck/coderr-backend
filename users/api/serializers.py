from rest_framework import serializers

from users.models import User, Profile


class RegistrationSerializer(serializers.ModelSerializer):

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

        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                "Passwords do not match"
            )

        return attrs

    def create(self, validated_data):

        validated_data.pop(
            "repeated_password"
        )

        return User.objects.create_user(
            **validated_data
        )


class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "location",
            "tel",
            "description",
            "uploaded_at",
        ]