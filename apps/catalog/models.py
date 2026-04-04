from django.db import models
from ..users.models import User
class Category(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='media/catalog/')
    slug = models.SlugField()
    

class Product(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2000, blank=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True)
    image = models.ImageField(upload_to='media/order/')
    brand = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    weight = models.CharField(max_length=68)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=False)
    

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete='CASCADE')
    product = models.ForeignKey(Product, related_name='favorites', on_delete='CASCADE')