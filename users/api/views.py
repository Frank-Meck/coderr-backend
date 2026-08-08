from django.http import request
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

from rest_framework.generics import (
    RetrieveUpdateAPIView,
    ListAPIView,
)
from .permissions import IsProfileOwner


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


class ProfileDetailView(RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated,
        IsProfileOwner,
    ]

    def get_queryset(self):
        return Profile.objects.filter(
            user_id=self.kwargs["pk"]
        )


class BusinessProfilesView(ListAPIView):
    """
    Returns all business profiles.
    """

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    queryset = Profile.objects.filter(
        user__type="business"
    )


class CustomerProfilesView(ListAPIView):
    """
    Returns all customer profiles.
    """

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    queryset = Profile.objects.filter(
        user__type="customer"
    )


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        print("LOGIN VIEW ERREICHT")
        print("REQUEST DATA:", request.data)

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
