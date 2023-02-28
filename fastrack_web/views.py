from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import RestaurantFilter
from .pagination import DefaultPagination
from .permissions import *


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
    ordering_fields = ['name']
    permission_classes = [IsRestaurantOrAdmin]
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated and user.user_type == 'R':
            if hasattr(user, 'restaurant'):
                raise PermissionDenied('A profile for this restaurant already exists')
            serializer.save(user=user)
        else:
            raise PermissionDenied('You must be a restaurant to create a profile')


    def perform_update(self, serializer):
        user = self.request.user
        # Only the authenticated customer user can update user_profile
        if user.is_authenticated and user.user_type == 'R':
            serializer.save(user=user)
        else:
            raise PermissionDenied('You must be a customer to update your profile')
    
    def list(self, request):
        user = self.request.user
        # An authenticated restaurant user can only view his/her user profile
        if user.is_authenticated and user.user_type == 'R':
            restaurant_profile = Restaurant.objects.get(user_id=request.user.id)
            serializer = self.get_serializer(restaurant_profile)
            return Response(serializer.data)
        # An authenticated super user can list all restaurant profiles
        else:
            return super().list(request)

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        user = self.request.user
        # An authenticated restaurant can use this end point
        if user.is_authenticated and user.user_type == 'R':
            restaurant_profile = Restaurant.objects.get(user_id=request.user.id)
            # An authenticated restaurant can view his/her profile
            if request.method == 'GET':
                serializer = self.get_serializer(restaurant_profile)
                return Response(serializer.data)
            elif request.method == 'PUT':
                serializer = RestaurantSerializer(restaurant_profile, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        else:
            return Response("Access Denied!", status=status.HTTP_405_METHOD_NOT_ALLOWED)

class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    # permission_classes = [IsAuthenticated, IsRestaurantOrReadOnly]

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
    # permission_classes = [IsAuthenticated]
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

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsCustomerOrAdmin]

    def perform_create(self, serializer):
        user = self.request.user
        # Only the authenticated customer user can create a customer profile
        if user.is_authenticated and user.user_type == 'C':
            serializer.save(user=user)
        else:
            raise PermissionDenied('You must be a customer to create a profile')

    def perform_update(self, serializer):
        user = self.request.user
        # Only the authenticated customer user can update user_profile
        if user.is_authenticated and user.user_type == 'C':
            serializer.save(user=user)
        else:
            raise PermissionDenied('You must be a customer to update your profile')
    
    def list(self, request):
        user = self.request.user
        # An authenticated customer user can only view his/her user profile
        if user.is_authenticated and user.user_type == 'C':
            customer_profile = Customer.objects.get(user_id=request.user.id)
            serializer = self.get_serializer(customer_profile)
            return Response(serializer.data)
        # An authenticated super user can list all customer profiles
        elif user.is_authenticated and user.user_type == 'S':
            return super().list(request)
        else:
            return Response("Access Denied!", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        user = self.request.user
        # An authenticated customer can use this end point
        if user.is_authenticated and user.user_type == 'C':
            customer_profile = Customer.objects.get(user_id=request.user.id)
            # An authenticated customer can view his/her profile
            if request.method == 'GET':
                serializer = self.get_serializer(customer_profile)
                return Response(serializer.data)
            elif request.method == 'PUT':
                serializer = CustomerSerializer(customer_profile, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        else:
            return Response("Access Denied!", status=status.HTTP_405_METHOD_NOT_ALLOWED)