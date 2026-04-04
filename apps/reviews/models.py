from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from ..catalog.models import Product
from ..users.models import User

class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete='CASCADE')
    product = models.ForeignKey(Product, related_name='reviews', on_delete='CASCADE')
    rating = models.IntegerField(max_length=10, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=500, blank=True)
    created_at = models.DateField(auto_now_add=True)