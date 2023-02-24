from rest_framework import permissions

class IsRestaurantOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and (request.user.user_type == 'R' or request.user.user_type == 'C'))
        return bool(request.user and request.user.user_type == 'R')