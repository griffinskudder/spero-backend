from rest_framework import viewsets

from authentication.models import User
from authentication.serializers import UserSerializer, CurrentUserSerializer
from spero.permissions import IsAuthenticatedOrOptions


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given user.
    list:
    Return all users.
    """
    queryset = User.objects.all().order_by('last_name', 'first_name')
    serializer_class = UserSerializer

    permission_classes = [IsAuthenticatedOrOptions]


class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given user (limited to the current user).
    list:
    Return all users (limited to the current user)
    """
    queryset = User.objects.none()
    serializer_class = CurrentUserSerializer

    permission_classes = [IsAuthenticatedOrOptions]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)
