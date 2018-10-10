from rest_framework.permissions import BasePermission


class AllowOnlyPost(BasePermission):
    """
    This permission allow only for POST request.
    Best use for registeration api view
    """

    SAFE_METHODS = ('POST',)

    def has_permission(self, request, view):
        return (
            request.method in self.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )
