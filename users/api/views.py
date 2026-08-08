from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    ListAPIView,
)
from django.contrib.auth import authenticate

from .serializers import RegistrationSerializer, ProfileSerializer
from .permissions import IsProfileOwner
from users.models import Profile


class RegistrationView(APIView):
    """
    Register a new user and return an authentication token.

    Allows unauthenticated users to create a customer or business account.
    After successful registration, an authentication token and basic user
    information are returned.

    Returns:
        201: User was successfully registered.
        400: Registration data is invalid.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Create a new user account.

        Args:
            request: HTTP request containing the registration data.

        Returns:
            Response: Authentication token and user information on success,
            or serializer validation errors on failure.
        """
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
    """
    Retrieve and update the profile of a specific user.

    Authenticated users can retrieve profile information.
    Profile updates are restricted to the owner of the profile.

    Returns:
        200: Profile was successfully retrieved or updated.
        401: User is not authenticated.
        403: Authenticated user is not the profile owner.
        404: Profile was not found.
    """

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated,
        IsProfileOwner,
    ]

    def get_queryset(self):
        """
        Return the profile belonging to the requested user ID.

        Returns:
            QuerySet: Profile matching the user ID from the URL.
        """
        return Profile.objects.filter(
            user_id=self.kwargs["pk"]
        )


class BusinessProfilesView(ListAPIView):
    """
    Return all profiles belonging to business users.

    Access to this endpoint requires authentication.

    Returns:
        200: List of business profiles.
        401: User is not authenticated.
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
    Return all profiles belonging to customer users.

    Access to this endpoint requires authentication.

    Returns:
        200: List of customer profiles.
        401: User is not authenticated.
    """

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    queryset = Profile.objects.filter(
        user__type="customer"
    )


class LoginView(APIView):
    """
    Authenticate a user and return an authentication token.

    Allows unauthenticated users to log in with their username and password.
    If the credentials are valid, an authentication token and basic user
    information are returned.

    Returns:
        200: Authentication was successful.
        400: Username/password is missing or credentials are invalid.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticate a user using the submitted credentials.

        Args:
            request: HTTP request containing username and password.

        Returns:
            Response: Authentication token and user information on success,
            or an error message if authentication fails.
        """
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
