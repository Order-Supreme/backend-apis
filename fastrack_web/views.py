from django.shortcuts import render, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


@api_view()
def home(request):
    return Response({"name": "Fast Track Restaurant System", "version": 1.0, "Developed by": "Zelalem Gizachew"})

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.prefetch_related('table_set', 'bookedtable_set', 'menu_set').all()
    serializer_class = RestaurantSerializer

class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

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
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer




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