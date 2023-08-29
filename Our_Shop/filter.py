

import django_filters
from .models import *

class ProductFilter(django_filters.FilterSet):
        
    class meta:
        model = Product
        fields = '__all__'
        exclude = ['price','digital','image']