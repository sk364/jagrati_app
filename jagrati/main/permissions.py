from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAnonymousUserForPOST(BasePermission):
    def has_permission(self, request, view):
        """
        Permission check for anonymous users for only POST request.
        """

        if type(request.user) is AnonymousUser:
            if request.method == 'POST':
                return True
        elif request.user.is_superuser:
            return True

        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Permission check if the `request.user` is the owner of `obj`
        """

        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
