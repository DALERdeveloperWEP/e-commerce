from django.db import models
from django.utils.translation import gettext_lazy as _

from ..users.models import User


class Category(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='catalog/')
    slug = models.SlugField()
    

class Product(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2000, blank=True)
    slug = models.SlugField(unique=True)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    card_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percent = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    image = models.ImageField(upload_to='order/')
    
    brand = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    weight = models.CharField(max_length=68)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    
    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='favorites', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')