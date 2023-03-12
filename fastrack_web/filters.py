from django_filters.rest_framework import FilterSet
from .models import Restaurant, BookedTable

class RestaurantFilter(FilterSet):
    class Meta:
        model = Restaurant
        fields = {
            'location': ['exact', 'icontains']
        }

# class BookedTableFilter(FilterSet):
#     # restaurant = filters.NumberFilter(field_name='restaurant__id')

#     class Meta:
#         model = BookedTable
#         fields = ['restaurant__id']