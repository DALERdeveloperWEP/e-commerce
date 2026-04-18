from django.db import models
from ..users.models import SellerProfile

class CategoryRequestChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CANCEL = 'cancel', 'Canceled'
    COMPLETED = 'completed', 'Completed'


class CategoryRequest(models.Model):
    seller = models.OneToOneField(SellerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='catalog/')
    slug = models.SlugField(unique=True)
    status = models.CharField(choices=CategoryRequestChoices.choices, default=CategoryRequestChoices.PENDING)