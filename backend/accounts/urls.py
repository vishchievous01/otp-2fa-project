from django.urls import path
from .views import LoginView, OTPVerifyView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('verify-otp', OTPVerifyView.as_view()),
]