from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name='travel-home'),
    url(r'^portfolio/$', views.portfolio, name='portfolio'),
    path('nearby',views.nearbylocations, name='nearby_location'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^confirm', views.sendItineraryEmail, name='confirm'),
    path('deals',views.deals, name='deals'),
     
]