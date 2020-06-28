from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.account_type
