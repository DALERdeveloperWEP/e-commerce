from rest_framework import serializers
from rest_framework.exceptions import NotFound
from django.contrib.auth.hashers import check_password

from .models import User
from .services import OTPService

class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()
    
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=16)
    
    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise NotFound(detail="Bunday Foydalanuvchi Mavjud Emas.")
        
        return value
        
    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError('Malumotlar Notogri Kiritildi')
        
        return super().validate(attrs)


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=16)
    confirm = serializers.CharField(min_length=6, max_length=16)
    
    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if user:
            raise serializers.ValidationError(detail="Bunday Foydalanuvchi Mavjud.")
        
        return value
        
    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        
        if attrs['password'] != attrs['confirm']:
            raise serializers.ValidationError('Parrol va Takrorlash Teng Emas')
        
        return super().validate(attrs) 
    

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verify_code = serializers.CharField(min_length=6, max_length=6)
    
    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise NotFound(detail="Bunday Foydalanuvchi Mavjud Emas.")
        
        return value
    
    def validate(self, attrs):
        otp = OTPService.get(attrs['email'])
        if not otp:
            raise serializers.ValidationError("Yaroq Siz Code.")
        
        if str(otp) != attrs['verify_code']:
            raise serializers.ValidationError("Kod noto'g'ri.")
        
        
        OTPService.delete(attrs['email'])
        
        return super().validate(attrs)