from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=124)
    slug = models.SlugField(unique=True)

    address = models.CharField(max_length=124)
    city = models.CharField(max_length=64, blank=True)
    region = models.CharField(max_length=64, blank=True)

    phone = models.CharField(max_length=15)

    latitude = models.FloatField()
    longitude = models.FloatField()

    work_start = models.TimeField()
    work_end = models.TimeField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name