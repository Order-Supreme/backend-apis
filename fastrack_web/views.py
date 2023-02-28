from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from .filters import RestaurantFilter
from .pagination import DefaultPagination
from .permissions import IsRestaurantOrReadOnly


@api_view()
def home(request):
    return Response({"name": "Fast Track Restaurant System", "version": 1.0, "Developed by": "Zelalem Gizachew"})

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RestaurantFilter
    pagination_class = DefaultPagination
    search_fields = ['name']
    order_fields = ['map_link']
    permission_classes = [IsRestaurantOrReadOnly]

    @action(detail=False, methods=['GET', 'PUT', 'POST'], permission_classes=[IsAuthenticated, IsRestaurantOrReadOnly])
    def me(self, request):
        # restaurant = Restaurant.objects.get(user_id=request.user.id)
        restaurant =  get_object_or_404(Restaurant, user=request.user.id)
        if request.method == 'GET':
            serializer = RestaurantSerializer(restaurant)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = RestaurantSerializer(restaurant, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOrReadOnly]

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(restaurant__user=self.request.user)
        return self.queryset

    

class PaymentViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

class ImageViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class BookedTableViewSet(ModelViewSet):
    queryset = BookedTable.objects.all()
    serializer_class = BookedTableSerializer

class OrderViewSet(ModelViewSet):
    # queryset = Order.objects.all()
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]
    # serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'R':
            isExist = Restaurant.objects.filter(user_id=user.id).exists()
            print(f'================ {user.id}')
            if isExist:
                restaurant_id = Restaurant.objects.only('restaurant_id').get(user_id=user.id)
                return Order.objects.prefetch_related('booked_table').filter(booked_table__restaurant=restaurant_id)
            else:
                return Order.objects.none()
                
        elif  user.user_type == 'C':
            customer_id = Customer.objects.only('customer_id').get(user_id=user.id)
            return Order.objects.prefetch_related('booked_table').filter(booked_table__customer=customer_id)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return CreateOrderSerializer
        else:
            return OrderSerializer



class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)



# @api_view(['GET', 'POST'])
# def restaurant_all(request):
#     if request.method == 'GET':
#         restaurant_dataset = Restaurant.objects.prefetch_related('table_set', 'bookedtable_set', 'menu_set').all()
#         serializers = RestaurantSerializer(restaurant_dataset, many=True)
#         return Response(serializers.data)
#     elif request.method == 'POST':
#         serializers = RestaurantSerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(serializers.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)