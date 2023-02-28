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

# class RestaurantViewSet(ModelViewSet):
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_class = RestaurantFilter
#     pagination_class = DefaultPagination
#     search_fields = ['name']
#     order_fields = ['map_link']
#     permission_classes = [IsRestaurantOrReadOnly]

#     def get_queryset(self):
#         if self.action == 'list':
#             return self.queryset.filter(user=self.request.user)
#         return self.queryset

#     @action(detail=False, methods=['GET', 'PUT', 'POST'], permission_classes=[IsAuthenticated, IsRestaurantOrReadOnly])
#     def me(self, request):
#         restaurant = get_object_or_404(Restaurant, user=request.user)
#         if request.method == 'GET':
#             serializer = RestaurantSerializer(restaurant)
#             return Response(serializer.data)
#         elif request.method == 'PUT':
#             serializer = RestaurantSerializer(restaurant, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)
