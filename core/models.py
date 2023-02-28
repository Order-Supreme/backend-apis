from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    USER_TYPES = [
        ('R', 'Restaurant'),
        ('C', 'Customer'),
        ('S', 'Super')
    ]
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default=USER_TYPES[2][0])