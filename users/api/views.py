from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny

from .serializers import RegistrationSerializer, ProfileSerializer
from users.models import Profile
from rest_framework.permissions import IsAuthenticated

class RegistrationView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegistrationSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
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