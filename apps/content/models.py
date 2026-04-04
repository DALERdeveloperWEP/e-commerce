from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to='media/content/')
    short_description = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)


class Vacancy(models.Model):
    title = models.CharField(max_length=128)
    requirements = models.CharField(max_length=128)
    responsibilities = models.CharField(max_length=128)
    conditions = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)