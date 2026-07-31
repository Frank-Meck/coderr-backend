from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """
    Allows users to edit only their own profile.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):
        return obj.user == request.user