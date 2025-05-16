from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    To implement a custom permission, override BasePermission and implement either,
    or both, of the following methods:

    .has_permission(self, request, view)
    .has_object_permission(self, request, view, obj)

    The methods should return True if the request should be granted access, and
    False otherwise.

    If you need to test if a request is a read operation or a write operation,
    you should check the request method against the constant SAFE_METHODS,
    which is a tuple containing 'GET', 'OPTIONS' and 'HEAD'.
    """

    message = "permission denied, you are not the owner"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
