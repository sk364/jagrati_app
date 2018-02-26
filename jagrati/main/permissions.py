from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission

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
