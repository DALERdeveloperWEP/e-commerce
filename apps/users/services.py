from random import randint

from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import User


class TokenService:
    
    @staticmethod
    def generate(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


    
class OTPService:
    
    @staticmethod
    def generate(email):
        otp = str(randint(100000, 999999))
        cache.set(email, otp, 120)
        return otp
    
    @staticmethod
    def get(email):
        return cache.get(email)
    
    @staticmethod
    def delete(email):
        cache.delete(email)
        return True
    
    def send_email(email, otp):
        try:
            subject = "Test OTP"
            text_content = f"OTP: {otp}"
            html_content = f"""
                <html>
                <body style="margin:0;padding:0;background:#0f172a;font-family:Arial,sans-serif;">

                    <div style="max-width:500px;margin:40px auto;padding:20px;">

                    <div style="
                        background:#1e293b;
                        border-radius:16px;
                        padding:32px;
                        text-align:center;
                    ">

                        <div style="
                        font-size:20px;
                        font-weight:bold;
                        margin-bottom:20px;
                        color:#38bdf8;
                        ">
                        🚀 MyApp
                        </div>

                        <div style="
                        font-size:22px;
                        font-weight:600;
                        margin-bottom:10px;
                        color:#e2e8f0;
                        ">
                        Tasdiqlash kodi
                        </div>

                        <div style="
                        font-size:14px;
                        color:#94a3b8;
                        margin-bottom:25px;
                        ">
                        Hisobingizga kirish uchun quyidagi koddan foydalaning
                        </div>

                        <div style="
                        font-size:36px;
                        letter-spacing:8px;
                        font-weight:bold;
                        background:#0f172a;
                        padding:16px;
                        border-radius:12px;
                        display:inline-block;
                        color:#38bdf8;
                        margin-bottom:20px;
                        ">
                        {otp}
                        </div>

                        <div style="
                        font-size:13px;
                        color:#64748b;
                        margin-top:20px;
                        ">
                        Bu kod 2 daqiqa amal qiladi. Hech kim bilan ulashmang.
                        </div>

                    </div>

                    </div>

                </body>
                </html>
                """

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            msg.attach_alternative(html_content, "text/html")

            result = msg.send(fail_silently=False)
            return result

        except Exception as e:
            print("EMAIL ERROR:", repr(e))
            raise