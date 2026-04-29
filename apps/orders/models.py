from django.db import models

from ..users.models import User
from ..catalog.models import Product

class StatusOrder(models.TextChoices):
    PENDING = 'pending', 'Pending' # — hali ko‘rilmagan
    CONFIRMED = 'confirmed', 'Confirmed' # — tasdiqlangan
    DELIVERED = 'delivered', 'Delivered' # — yetkazilgan
    CANCELLED = 'cancelled', 'Cancelled' # — bekor qilingan


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=32)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=64)
    house = models.CharField(max_length=32)
    apartment = models.CharField(max_length=32)
    comment = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=StatusOrder.choices, default=StatusOrder.PENDING)
    total_price = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.full_name}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    price = models.FloatField()