from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)