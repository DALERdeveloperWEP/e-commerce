from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.views import APIView, Request, Response
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import GoogleAuthSerializer, LoginSerializer, RegisterSerializer, VerifyOTPSerializer
from .services import TokenService, OTPService

class GoogleAuthView(APIView):
    def post(self, request: Request):
        serializer = GoogleAuthSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data['token']
            
            try:
                idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)            
            except ValueError as e:
                print(e)
                return Response({"error": "Invalid token"}, status=400)

            user, created = User.objects.get_or_create(
                email=idinfo['email'],
                defaults={
                    'first_name': idinfo['given_name'],
                    'username': idinfo['email'].split('@')[0],
                }
            )
            
            return Response(TokenService.generate(user))


class LoginView(APIView):
    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']            
            user = User.objects.filter(email=email).first()

            OTPService.send_email(email, OTPService.generate(email))
            
            return Response({"success": "Tizimga Kirish muvaffaqiyatli amalga oshirildi. Iltimos, emailingizni tekshiring va tasdiqlash kodini kiriting."})
            
            
class RegisterView(APIView):
    def post(self, request: Request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = User.objects.create(
                email=email,
                first_name=name,
                username=email.split('@')[0],
            )
            user.set_password(password)
            user.save()
            
            OTPService.send_email(email, OTPService.generate(email))
            
            return Response({"success": "Ro'yhatdan o'tish muvaffaqiyatli amalga oshirildi. Iltimos, emailingizni tekshiring va tasdiqlash kodini kiriting."})
            

class VerifyOTPView(APIView):
    def post(self, request: Request):
        serializser = VerifyOTPSerializer(data=request.data)
        
        if serializser.is_valid(raise_exception=True):
            email = serializser.validated_data['email']
            user = User.objects.filter(email=email).first()
            return Response(TokenService.generate(user))
        


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request):
        user = request.user
        return Response({
            "email": user.email,
            "name": user.first_name,
            "role": user.role,
            "is_seller": user.is_seller,
            "phone": user.phone,
            "logo": user.logo.url if user.logo else None,
        })