from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """
    Allows profile editing only for the owner.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):
        if request.method == "GET":
            return True

        return obj.user == request.user
