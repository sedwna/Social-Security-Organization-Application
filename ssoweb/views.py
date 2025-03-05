from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OTP
import random
# Create your views here.


class SendOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")

        if not phone_number or len(phone_number) != 11:
            return Response({"error": "شماره تلفن معتبر نیست."}, status=status.HTTP_400_BAD_REQUEST)

        otp, created = OTP.objects.get_or_create(phone_number=phone_number)
        otp.generate_otp()

        # در اینجا باید کد OTP را از طریق SMS ارسال کنیم
        # print(f"OTP: {otp.code}")  # فقط برای تست

        return Response({"message": "کد تأیید ارسال شد."}, status=status.HTTP_200_OK)


from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class VerifyOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        code = request.data.get("code")

        try:
            otp = OTP.objects.get(phone_number=phone_number)
        except OTP.DoesNotExist:
            return Response({"error": "کد نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

        if otp.code != code or not otp.is_valid():
            return Response({"error": "کد تأیید اشتباه یا منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(phone_number=phone_number, defaults={"username": phone_number})

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"message": "ورود موفق!", "token": token.key}, status=status.HTTP_200_OK)
