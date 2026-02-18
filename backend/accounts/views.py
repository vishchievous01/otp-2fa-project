from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pyotp
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTP
from .utils import generate_otp_secret, verify_otp


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        OTP.objects.filter(user=user, is_verified=False).delete()

        secret = generate_otp_secret()
        otp_obj = OTP.objects.create(user=user, secret=secret)

        totp = pyotp.TOTP(secret)
        print("OTP:", totp.now())

        return Response(
            {
                "message": "OTP sent",
                "pre_auth_token": str(otp_obj.pre_auth_token)
            },
            status=status.HTTP_200_OK
        )


class OTPVerifyView(APIView):
    def post(self, request):
        token = request.data.get("pre_auth_token")
        otp = request.data.get("otp")

        if not token or not otp:
            return Response(
                {"error": "pre_auth_token and otp required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_obj = (
            OTP.objects
            .filter(pre_auth_token=token, is_verified=False)
            .order_by("-created_at")
            .first()
        )

        if not otp_obj:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp_obj.attempts >= settings.MAX_OTP_ATTEMPTS:
            return Response(
                {"error": "OTP locked"},
                status=status.HTTP_403_FORBIDDEN
            )

        if verify_otp(otp_obj.secret, otp):
            otp_obj.is_verified = True
            otp_obj.save()

            refresh = RefreshToken.for_user(otp_obj.user)

            return Response(
                {
                    "message": "Authentication successful",
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                },
                status=status.HTTP_200_OK
            )

        otp_obj.attempts += 1
        otp_obj.save()

        return Response(
            {"error": "Invalid OTP"},
            status=status.HTTP_400_BAD_REQUEST
        )
