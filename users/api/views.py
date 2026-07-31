from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny

from .serializers import RegistrationSerializer, ProfileSerializer
from users.models import Profile
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class RegistrationView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            token, created = Token.objects.get_or_create(
                user=user
            )

            return Response(
                {
                    "token": token.key,
                    "username": user.username,
                    "email": user.email,
                    "user_id": user.id,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        profile = Profile.objects.get(
            user=request.user
        )

        serializer = ProfileSerializer(profile)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {
                    "detail": "Username and password are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return Response(
                {
                    "detail": "Invalid credentials"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_200_OK
        )
