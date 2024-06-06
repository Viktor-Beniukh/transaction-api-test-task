from drf_spectacular.utils import extend_schema_view, extend_schema

from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserSerializer, AuthTokenSerializer, AdminSerializer


@extend_schema_view(
    post=extend_schema(
        description="Create a new admin",
        request=AdminSerializer,
        responses={201: AdminSerializer},
    ),
)
class CreateAdminView(generics.CreateAPIView):
    serializer_class = AdminSerializer


@extend_schema_view(
    post=extend_schema(
        description="Logining existing admin and receiving a token authorisation",
        request=AuthTokenSerializer,
        responses={200: AuthTokenSerializer},
    ),
)
class LoginAdminView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


@extend_schema_view(
    post=extend_schema(
        description="Logout admin from the system",
        request=None,
        responses={
            200: {
                "description": "Admin has logged out successfully",
                "content": {
                    "application/json": {
                        "example": {"detail": "You have logged out successfully!"}
                    }
                },
            },
            401: {
                "description": "Error: Unauthorized",
                "content": {
                    "application/json": {
                        "examples": {
                            "authentication_error": {
                                "detail": "Authentication credentials were not provided."
                            },
                            "invalid_authentication_token": {
                                "detail": "Invalid token."
                            },
                        }
                    }
                },
            },
        },
    ),
)
class LogoutAdminView(APIView):
    serializer_class = None
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"message": "You have logged out successfully!"},
            status=status.HTTP_200_OK,
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    @extend_schema(
        description="Obtain list of users",
        responses={200: UserSerializer},
    )
    def list(self, request, *args, **kwargs):
        """Get list of users"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Retrieve a specific user",
        responses={200: UserSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific user"""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Create a new user",
        request=UserSerializer,
        responses={201: UserSerializer},
    )
    def create(self, request, *args, **kwargs):
        """Create a new user"""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing user",
        request=UserSerializer,
        responses={200: UserSerializer},
    )
    def update(self, request, *args, **kwargs):
        """Update an existing user"""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing user",
        request=UserSerializer,
        responses={200: UserSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update an existing user"""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="Delete an existing user",
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an existing user"""
        return super().destroy(request, *args, **kwargs)
