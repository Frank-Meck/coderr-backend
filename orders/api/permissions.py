from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """
    Permission class that allows access only to authenticated
    users with the customer user type.
    """

    def has_permission(self, request, view):
        """
        Check whether the requesting user is an authenticated customer.

        Returns True if the user is authenticated and has the
        customer user type. Otherwise, returns False.
        """
        return (
            request.user.is_authenticated
            and request.user.type == "customer"
        )
