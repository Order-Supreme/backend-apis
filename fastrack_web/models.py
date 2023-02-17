from django.db import models


class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    map_link = models.TextField(null=True)
    location = models.TextField(null=False)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=255, null=False)


class Table(models.Model):
    table_id = models.AutoField(primary_key=True)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    no_of_seats = models.PositiveSmallIntegerField(default=1)
    isBooked = models.BooleanField(default=False)
    createdOn = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    payment_method = models.BooleanField(default=False)
    credit_card_info = models.TextField(blank=True, null=True)
    createdOn = models.DateTimeField(auto_now_add=True)


class BookedTable(models.Model):
    booked_id = models.AutoField(primary_key=True)
    no_of_peoples = models.PositiveSmallIntegerField(default=1)
    booking_time_x = models.DateTimeField(null=False)
    booking_time_y = models.DateTimeField(null=False)
    createdOn = models.DateTimeField(auto_now_add=True)
    isCancelled = models.BooleanField(default=False)
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_path = models.CharField(max_length=255)
    createdOn = models.DateTimeField(auto_now_add=True)


class Menu(models.Model):
    dish_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField()
    isSpecial = models.TextField(default=None)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    images = models.ForeignKey(Images, on_delete=models.PROTECT)


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
        max_length=100, choices=ORDER_STATUS, default=ORDER_STATUS[0])
    booked_table = models.ForeignKey(BookedTable, on_delete=models.PROTECT)
    dish = models.ManyToManyField(Menu)


class Payments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey('Order', on_delete=models.PROTECT)
    user_id = models.ForeignKey('User', on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    createdOn = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
