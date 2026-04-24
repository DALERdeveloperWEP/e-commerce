from django.db import models
from ..users.models import SellerProfile

class CategoryRequestChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CANCEL = 'cancel', 'Canceled'
    COMPLETED = 'completed', 'Completed'


class CategoryRequest(models.Model):
    seller = models.ForeignKey(SellerProfile, related_name='category_request', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='catalog/')
    slug = models.SlugField(unique=True)
    status = models.CharField(choices=CategoryRequestChoices.choices, default=CategoryRequestChoices.PENDING)
    comment = models.CharField(max_length=500)
    cancelled_by_role = models.CharField(blank=True, null=True, default='seller')
    
    def __str__(self):
        return self.name