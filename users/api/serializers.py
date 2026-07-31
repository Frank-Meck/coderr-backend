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
