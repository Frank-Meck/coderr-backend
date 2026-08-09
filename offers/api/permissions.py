"""
Custom permissions for the offers API.

Defines permissions for restricting offer creation to business
users and ensuring that only offer owners can modify or delete
their offers.
"""

from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """
    Allow access only to authenticated business users.
    """

    def has_permission(self, request, view):
        """
        Check whether the requesting user is an authenticated business user.
        """

        return (
            request.user.is_authenticated
            and request.user.type == "business"
        )


class IsOfferOwner(BasePermission):
    """
    Allow access only to the owner of an offer.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user owns the given offer.
        """

        return obj.business == request.user
