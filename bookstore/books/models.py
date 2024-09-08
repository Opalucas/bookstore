from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Cart(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.CharField(default='', max_length=255)
    quntity = models.IntegerField(default=0)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    product = models.CharField(max_length=255, default='') 
    quantity = models.IntegerField(default=0) 
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class Addres(models.Model):
    street = models.CharField(max_length=255, default='')
    neighborhood = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    number = models.IntegerField(default=0)