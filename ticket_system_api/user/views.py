"""Views for the user API."""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer
from core.custom_permissions import IsAdminOrForbidden


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system. """

    serializer_class = UserSerializer
    permission_classes = [IsAdminOrForbidden, permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self):
        """Retrieve and return the authenticated user."""

        return self.request.user
