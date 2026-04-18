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
    


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=124, blank=True)
    gender = models.CharField(max_length=7, blank=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True, validators=[phone_validator])
    

    
user = {
  "email": str,
  "first_name": str,
  "last_name": str | None,
  "role": "str",
  "is_seller": bool,
  "phone": None | str,
  "logo": None | str,
  "cashback": None | float, # Yoki umuman kelmasligi ham mumkin
  "gender": None | str,
  "is_card": bool, # Yoki umuman kelmasligi ham mumkin (sababi menagerni card qosholmaydi)
}

admin_response = {
    "users": {
        "first_name": str,
        "last_name": str,
        "phone": str,
        "logo": str,
        "gender": str,
        "is_card": bool,
    },
    "seller": {
        "first_name": str,
        "last_name": str,
        "phone": str,
        "logo": str,
        "gender": str,
        # product kelmaydi sababi backend tomonlama code kopayib ketadi shuning uchun uni boshqa api dan olinadi 
    }
}