from django.db import models
from django.conf import settings



class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    map_link = models.TextField(null=True)
    location = models.TextField(null=False)
    phone_number = models.CharField(max_length=20, null=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.restaurant_id)




class Table(models.Model):
    table_id = models.AutoField(primary_key=True)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    no_of_seats = models.PositiveSmallIntegerField(default=1)
    isVIP = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isBooked = models.BooleanField(default=False)
    createdOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.table_id)




class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    payment_method = models.BooleanField(default=False)
    credit_card_info = models.TextField(blank=True, null=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.customer_id)



class BookedTable(models.Model):
    booked_id = models.AutoField(primary_key=True)
    no_of_peoples = models.PositiveSmallIntegerField(default=1)
    booking_time_x = models.DateTimeField(null=False)
    booking_time_y = models.DateTimeField(null=False)
    createdOn = models.DateTimeField(auto_now_add=True)
    isCancelled = models.BooleanField(default=False)
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.booked_id)




class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_path = models.CharField(max_length=255)
    createdOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.image_id)




class Menu(models.Model):
    dish_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isSpecial = models.BooleanField(default=False)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    images = models.ForeignKey(Images, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.dish_id)



class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    inventory_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    measurement = models.CharField(max_length=40, null=True)
    notice_if_below = models.PositiveIntegerField(default=10)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)
    update_remark = models.TextField(default=None)

    def __str__(self):
        return str(self.inventory_id)



class Order(models.Model):
    ORDER_STATUS = [
        ('P', 'Placed'),
        ('K', 'In Kitchen'),
        ('R', 'Ready'),
        ('D', 'Delivered')
    ]
    order_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    order_item = models.CharField(max_length=100)
    quantity = models.PositiveSmallIntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    order_status = models.CharField(
        max_length=100, choices=ORDER_STATUS, null=True, default=None)
    wait_time = models.TimeField(null=True)
    isTakeaway = models.BooleanField(default=False)
    createdOn = models.DateTimeField(auto_now_add=True)
    booked_table = models.ForeignKey(BookedTable, on_delete=models.PROTECT)
    inventories = models.ForeignKey(Inventory, on_delete=models.PROTECT, null=True, default=None)
    dish = models.ManyToManyField(Menu)

    def __str__(self):
        return str(self.order_id
)



class Payments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    createdOn = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    orders = models.ForeignKey(Order, on_delete=models.PROTECT)
    customers = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.payment_id)


