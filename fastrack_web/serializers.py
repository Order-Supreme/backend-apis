from .models import *


from rest_framework import serializers




class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['inventory_id', 'inventory_name', 'quantity', 'measurement', 'notice_if_below', 'createdOn', 'updatedOn', 'update_remark', 'restaurant']


class BookedTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedTable
        fields = ['booked_id', 'no_of_peoples', 'booking_time_x', 'booking_time_y', 'createdOn', 'isCancelled', 'table', 'restaurant', 'customer']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['dish_id', 'name', 'description', 'price', 'isSpecial', 'createdOn', 'updatedOn', 'restaurant']
        read_only_fields = ['createdOn', 'updatedOn']
        required_fields = ['name', 'description', 'price']

# class MenuCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Menu
#         fields = ['dish_id', 'name', 'description', 'price', 'isSpecial', 'createdOn', 'updatedOn', 'image_id']
#         read_only_fields = ['createdOn', 'updatedOn']

class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model = Order
        fields = ['order_id', 'customer_name', 'quantity', 'total_price', 'special_requests', 'order_status', 'wait_time', 'isTakeaway', 'createdOn', 'booked_table', 'dish', 'inventories']
    
    booked_table = BookedTableSerializer(required=True)
    dish = MenuSerializer(many=True, required=True)

    def get_total_price(self, order: Order):
        return 0

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'customer_name', 'quantity', 'special_requests', 'isTakeaway', 'booked_table', 'dish']

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('id', 'createdOn', 'image', 'image_path')
        read_only_fields = ('id', 'createdOn', 'image_path')


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['payment_id', 'total_amount', 'payment_method', 'createdOn', 'payment_status', 'orders', 'customers']
    


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['table_id', 'no_of_seats', 'isVIP', 'price', 'isBooked', 'createdOn', 'restaurant']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['customer_id', 'user_id', 'phone_number', 'payment_method', 'credit_card_info', 'createdOn']


class RestaurantSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Restaurant
        fields = ['restaurant_id', 'user_id', 'name', 'map_link', 'location', 'phone_number']

    # table_set = TableSerializer(many=True, required=False)
    # bookedtable_set = BookedTableSerializer(many=True, required=False)
    # menu_set = MenuSerializer(many=True, required=False)


