from django.contrib import admin
from .models import *
# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code','discountPercentage']
    list_filter = ['code','discountPercentage']

admin.site.register(Coupons,CouponAdmin)

class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name','country','cost','days','package','rating','image','date_posted','hits']

admin.site.register(Destinations,DestinationAdmin)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ['user','destination_id','destination_name']
    
admin.site.register(Orders,OrdersAdmin)