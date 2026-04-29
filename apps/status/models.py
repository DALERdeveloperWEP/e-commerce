from django.db import models
from ..users.models import SellerProfile

class TaskStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    DONE = 'done', 'Done'
    

class TaskPriority(models.TextChoices):
    HIGH = 'high', 'High'
    MEDIUM = 'medium', 'Medium'
    LOW = 'low', 'Low'

class Tasks(models.Model):
    seller = models.ForeignKey(SellerProfile, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    time = models.DateTimeField()
    status = models.CharField(choices=TaskStatus.choices, default=TaskStatus.PENDING)
    priority = models.CharField(choices=TaskPriority.choices, default=TaskPriority.MEDIUM)