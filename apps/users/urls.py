from django.urls import path
from .views import GoogleAuthView, LoginView, RegisterView, UserProfileView, VerifyOTPView

urlpatterns = [
    path('google/', GoogleAuthView.as_view(), name='google_auth'),
    path('login/', LoginView.as_view(), name='login_auth'),
    path('register/', RegisterView.as_view(), name='register_auth'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp_auth'),
    path('profile/', UserProfileView.as_view(), name='profile_auth'),
]
