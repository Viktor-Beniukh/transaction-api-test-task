from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserSerializer, AuthTokenSerializer, AdminSerializer


class CreateAdminView(generics.CreateAPIView):
    serializer_class = AdminSerializer


class LoginAdminView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


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
