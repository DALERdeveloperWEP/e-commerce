from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+998 \d{2} \d{3} \d{2} \d{2}$',
    message="+998 xx xxx xx xx formatida kiriting"
)

class User(AbstractUser):
    class RoleChoice(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'
        SELLER = 'seller', 'Seller'
        
    role = models.CharField(max_length=7, blank=True, default=RoleChoice.USER)
    phone = models.CharField(max_length=15, unique=True, validators=[phone_validator])
    
    

