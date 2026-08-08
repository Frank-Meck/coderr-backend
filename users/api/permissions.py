from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """
    Allow users to edit only their own profile.

    Profile data can be viewed by authenticated users, but profile
    modifications are restricted to the user who owns the profile.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):
        """
        Check whether the requesting user may access or modify the profile.

        GET requests are allowed for authenticated users.
        All other requests require the requesting user to own the profile.

        Args:
            request: The incoming HTTP request.
            view: The view associated with the request.
            obj: The Profile instance being accessed.

        Returns:
            bool: True if the request is allowed, otherwise False.
        """
        if request.method == "GET":
            return True

        return obj.user == request.user