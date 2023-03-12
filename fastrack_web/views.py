import os, io
from django.shortcuts import get_object_or_404, HttpResponse
from django.http import FileResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from PIL import Image
from .models import *
# from .models import Images as ImageModel
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
            isExist = Restaurant.objects.filter(user_id=request.user.id).exists()
            if isExist:
                restaurant_profile = Restaurant.objects.get(user_id=request.user.id)
                serializer = self.get_serializer(restaurant_profile)
                return Response(serializer.data)
            else:
                return Response("Your Profile has not been created yet!", status=status.HTTP_404_NOT_FOUND)
        # An authenticated super user can list all restaurant profiles
        else:
            return super().list(request)

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        user = self.request.user
        # An authenticated restaurant can use this end point
        if user.is_authenticated and user.user_type == 'R':
            isExist = Restaurant.objects.filter(user_id=request.user.id).exists()
            if isExist:
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
                return Response("Your Profile has not been created yet!", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Access Denied!", status=status.HTTP_405_METHOD_NOT_ALLOWED)

class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restaurant']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.user_type == 'R':
            if not hasattr(user, 'restaurant'):
                raise PermissionDenied('A profile for this restaurant does not exists')
            return Table.objects.filter(restaurant=user.restaurant)
        elif user.is_authenticated and user.user_type == 'C':
            return Table.objects.all()
        return Table.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated and user.user_type == 'R' and user.restaurant == serializer.validated_data['restaurant']:
            restaurant = self.request.user.restaurant
            serializer.save(restaurant=restaurant)
        else:
            raise PermissionDenied('You are not authorized to perform this action')

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_authenticated and user.user_type == 'R' and user.restaurant == serializer.validated_data['restaurant']:
            restaurant = self.request.user.restaurant
            serializer.save(restaurant=restaurant)
        else:
            raise PermissionDenied('You are not authorized to perform this action')

    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_authenticated and user.user_type == 'R' and user.restaurant == instance.restaurant:
            instance.delete()
        else:
            raise PermissionDenied('You are not authorized to perform this action')

    

class PaymentViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

class ImageViewSet(ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageUploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(image_path=serializer.validated_data['image'].name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
        image = Image.open(image_path)

        # Convert the image to RGB mode
        image = image.convert("RGB")
        response = HttpResponse(content_type="image/jpeg")
        image.save(response, "JPEG")
        return response
        # return Response(img_bytes.read(), content_type='image/jpeg')

class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.none()
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restaurant']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.user_type == 'R':
                return Menu.objects.filter(restaurant__user=self.request.user)
            elif self.request.user.user_type == 'C':
                return Menu.objects.all()
        return Menu.objects.none()

    def get_restaurant(self):
        user = self.request.user
        if user.is_authenticated and user.user_type == 'R':
            restaurant = user.restaurant
            if restaurant is not None:
                return restaurant
        return None

    def create(self, request, *args, **kwargs):
        restaurant = self.get_restaurant()
        if restaurant is not None:
            # image_id = request.data.get('image')
            # if image_id:
            #     try:
            #         image = ImageModel.objects.get(pk=image_id)
            #     except ImageModel.DoesNotExist:
            #         return Response({'image_id': 'Invalid image id'}, status=status.HTTP_400_BAD_REQUEST)
            # else:
            #     return Response({'image_id': 'Image id is required'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = MenuSerializer(data=request.data)
            if serializer.is_valid():
                # menu = serializer.save(restaurant=restaurant, image=image)
                menu = serializer.save(restaurant=restaurant)
                return Response(MenuSerializer(menu).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_authenticated and user.user_type == 'R' and user.restaurant == instance.restaurant:
            instance.delete()
        else:
            raise PermissionDenied('You are not authorized to perform this action')


class BookedTableViewSet(ModelViewSet):
    queryset = BookedTable.objects.all()
    serializer_class = BookedTableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restaurant']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'C':
            isExist = BookedTable.objects.filter(customer=user.id).exists()
            if isExist:
                return BookedTable.objects.filter(customer=user.customer)
            return BookedTable.objects.none()
        elif user.user_type == 'R':
            isExist = BookedTable.objects.filter(restaurant=user.id).exists()
            if isExist:
                return BookedTable.objects.filter(restaurant=user.id)
            return BookedTable.objects.none()
        return BookedTable.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated and user.user_type == 'C':
            customer = self.request.user.customer
            serializer.save(customer=customer)

    

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
            isExist = Customer.objects.filter(user_id=user.id).exists()
            if isExist:
                customer_id = Customer.objects.only('customer_id').get(user_id=user.id)
                return Order.objects.prefetch_related('booked_table').filter(booked_table__customer=customer_id)
            else:
                return Response("Your Profile has not been created yet!", status=status.HTTP_404_NOT_FOUND)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return CreateOrderSerializer
        else:
            return OrderSerializer

    # @action(detail=True, methods=['GET', 'PUT'])
    # def inventory(self, request):
    #     user = self.request.user
    #     # An authenticated customer can use this end point
    #     if user.is_authenticated and user.user_type == 'R':
    #         if request.method == 'PUT':
    #             serializer = OrderSerializer()
    #             serializer.is_valid(raise_exception=True)
    #             serializer.save()
    #             return Response(serializer.data)
    #     else:
    #         return Response("Access Denied!", status=status.HTTP_405_METHOD_NOT_ALLOWED)


class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.none()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.user_type == 'R':
            # return inventories that belong to the restaurant of the authenticated restaurant owner
            return Inventory.objects.filter(restaurant=user.restaurant)
        else:
            # return an empty queryset if the user is not authenticated or not a restaurant owner
            return Inventory.objects.none()

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
            isExist = Customer.objects.filter(user_id=request.user.id).exists()
            if isExist:
                customer_profile = Customer.objects.get(user_id=request.user.id)
                serializer = self.get_serializer(customer_profile)
                return Response(serializer.data)
            else:
                return Response("Your Profile has not been created yet!", status=status.HTTP_404_NOT_FOUND)
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
            isExist = Customer.objects.filter(user_id=user.id).exists()
            if isExist:
                customer_profile = Customer.objects.get(user_id=user.id)
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
                return Response("Your Profile has not been created yet!", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Access Denied!", status=status.HTTP_405_METHOD_NOT_ALLOWED)