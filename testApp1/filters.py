import django_filters 
from .models import *

class DestinationsFilter(django_filters.FilterSet):
    class Meta:
        model = Destinations
        fields = {
            'name':['icontains'],
            'country':['icontains'],
            'rating':['icontains'],
            #'image' :['icontains'],
        }