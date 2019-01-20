from rest_framework import permissions


class IsAuthenticatedOrOptions(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return super().has_permission(request, view)


class IsAdminUserOrOptions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return super().has_permission(request, view)


class IsAdminUserOrAuthenticatedAndReadOnlyOrOptions(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
            request.method == 'OPTIONS' or
            request.method in permissions.SAFE_METHODS and
            request.user and request.user.is_authenticated or
            request.user and request.user.is_staff
        )
