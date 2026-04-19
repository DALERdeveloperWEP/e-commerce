from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="+998 xx xxx xx xx formatida kiriting"
)

class User(AbstractUser):
    class RoleChoice(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'
        SELLER = 'seller', 'Seller'
        
    role = models.CharField(max_length=7, blank=True, default=RoleChoice.USER)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True, validators=[phone_validator])
    logo = models.ImageField(upload_to='media/user/user_logos/', blank=True, null=True)
    is_seller = models.BooleanField(default=False)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=124, blank=True)
    is_card = models.BooleanField(default=False)
    gender = models.CharField(max_length=7, blank=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True, validators=[phone_validator])
    cashback = models.FloatField(default=0)
    
    def __str__(self):
        return self.FullName


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=124, blank=True)
    gender = models.CharField(max_length=7, blank=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True, validators=[phone_validator])
    
    def __str__(self):
        return self.FullName
    

