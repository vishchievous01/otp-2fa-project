from rest_framework import serializers

class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField()