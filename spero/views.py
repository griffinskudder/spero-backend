from django.contrib.auth import login

from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

from spero.permissions import IsAuthenticatedOrOptions


class LoginView(KnoxLoginView):
    """
    Get an auth token for the user if correct credentials are provided.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class LogoutView(KnoxLogoutView):
    """
    Delete the auth token for the current session.
    """
    permission_classes = (IsAuthenticatedOrOptions,)
