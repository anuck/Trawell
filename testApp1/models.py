from django.db import models
from django.utils import timezone

class Destinations(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    cost=models.IntegerField(default=0)
    days=models.IntegerField(default=0)
    package = models.CharField(max_length=100)
    rating = models.FloatField(default='1')
    image = models.TextField(default='Canada-Montreal')
    date_posted= models.DateTimeField(default=timezone.now)
    hits = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Coupons(models.Model):
    code=models.CharField(max_length=100)
    discountPercentage=models.IntegerField(default=0)

class Orders(models.Model):
    user = models.CharField(max_length=100)
    destination_id = models.IntegerField(default=0)
    destination_name = models.CharField(max_length=100)
    