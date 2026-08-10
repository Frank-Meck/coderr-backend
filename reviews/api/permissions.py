from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """
    Permission class that allows access only to authenticated customers.
    """

    def has_permission(
        self,
        request,
        view,
    ):
        """
        Checks whether the current user is authenticated and a customer.
        """

        return (
            request.user.is_authenticated
            and request.user.type == "customer"
        )
