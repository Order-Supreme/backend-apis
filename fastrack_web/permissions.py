from rest_framework import permissions


class IsRestaurantOrReadOnly(permissions.BasePermission):
    """
    Allows access only to restaurant owners for editing and deleting their own data
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.user_type == 'R'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsRestaurantOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or obj.user.user_type == 'C':
            return request.method in permissions.SAFE_METHODS # allow read-only for admin
        elif obj.user == request.user and obj.user.user_type == 'R':
            return True # allow restaurant to read and update their own profile
        else:
            return False

class IsCustomerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or obj.user.user_type == 'R':
            return request.method in permissions.SAFE_METHODS # allow read-only for admin & restaurant
        elif obj.user == request.user and obj.user.user_type == 'C':
            return True # allow customer to read and update their own profile
        else:
            return False