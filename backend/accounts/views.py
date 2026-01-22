from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from .models import OTP
from .utils import generate_otp_secret, verify_otp

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=401)
        
        secret = generate_otp_secret()
        OTP.objects.create(user=user, secret=secret)

        import pyotp
        totp = pyotp.TOTP(secret)
        print("OTP:", totp.now())

        return Response({"message": "OTP sent"}, status=200)

class OTPVerifyView(APIView):
    def post(self, request):
        otp = request.data.get("otp")
        user = request.user

        otp_obj = OTP.objects.filter(user=user, is_verified=False)

        if not otp_obj:
            return Response({"error": "OTP not found"}, status=400)
        
        if verify_otp(otp_obj.secret, otp):
            otp_obj.is_verified = True
            otp_obj.save()
            return Response({"message": "Authentication successful"}, status=200)
        
        return Response({"error": "Invalid OTP"}, status=400)