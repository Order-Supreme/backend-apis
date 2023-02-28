from rest_framework import permissions

# class IsRestaurantOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return bool(request.user and (request.user.user_type == 'R' or request.user.user_type == 'C'))
#         return bool(request.user and request.user.user_type == 'R')

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


class IsCustomerOrReadOnly(permissions.BasePermission):
    """
    Allows access only to customers for editing and deleting their own data
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.user_type == 'C'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsRestaurantOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return request.method in permissions.SAFE_METHODS # allow read-only for admin
        elif obj.user == request.user and obj.user.user_type == 'R':
            return True # allow customer to read and update their own profile
        else:
            return False

class IsCustomerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return request.method in permissions.SAFE_METHODS # allow read-only for admin
        elif obj.user == request.user and obj.user.user_type == 'C':
            return True # allow customer to read and update their own profile
        else:
            return False




# class CustomerProfileViewSet(ModelViewSet):
#     queryset = CustomerProfile.objects.all()
#     serializer_class = CustomerProfileSerializer
#     permission_classes = [IsCustomerOrAdmin]

#     def perform_create(self, serializer):
#         user = self.request.user
#         if user.is_authenticated and user.user_type == 'customer':
#             serializer.save(user=user)
#         else:
#             raise PermissionDenied('You must be a customer to create a profile')

#     def perform_update(self, serializer):
#         user = self.request.user
#         if user.is_authenticated and user.user_type == 'customer':
#             serializer.save(user=user)
#         else:
#             raise PermissionDenied('You must be a customer to update your profile')

#     @action(detail=False, methods=['get'])
#     def my_profile(self, request):
#         customer_profile = CustomerProfile.objects.get(user=request.user)
#         serializer = self.get_serializer(customer_profile)
#         return Response(serializer.data)
