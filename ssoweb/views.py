from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer  # فرض کنید یک Serializer برای CustomUser دارید
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class SendOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")

        if not phone_number:
            return Response({"error": "شماره تماس ضروری است!"}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی وود شماره تلفن در سیستم
        # try:
        #     user = CustomUser.objects.get(phone_number=phone_number)
        # except CustomUser.DoesNotExist:
        #     return Response({"error": "این شماره تماس در سیستم ثبت نشده است."}, status=status.HTTP_400_BAD_REQUEST)

        # تولید کد OTP
        otp_code = str(random.randint(1000, 9999))

        # ذخیره OTP در دیتابیس
        otp, created = OTP.objects.get_or_create(phone_number=phone_number)
        otp.code = otp_code
        otp.is_valid = True
        otp.save()

        return Response({"message": f"کد تایید {otp_code} به شماره {phone_number} ارسال شد."},
                        status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        code = request.data.get("code")

        if not phone_number or not code:
            return Response({"error": "شماره تماس و کد تایید ضروری است!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp = OTP.objects.get(phone_number=phone_number, code=code)
        except OTP.DoesNotExist:
            return Response({"error": "کد تایید اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)

        # if otp.is_expired():
        #     return Response({"error": "کد تایید منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)

        # گرفتن تمامی شماره تماس‌های موجود در CustomUser
        allowed_phone_numbers = CustomUser.objects.values_list('phone_number', flat=True)

        if phone_number not in allowed_phone_numbers:
            return Response({"error": "شما مجاز به ورود نیستید."}, status=status.HTTP_403_FORBIDDEN)

        # بررسی وجود کاربر
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({"error": "ثبت نام نکردید. ابتدا ثبت نام کنید."}, status=status.HTTP_400_BAD_REQUEST)

        # ایجاد توکن برای کاربر
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"message": "ورود موفق!", "token": token.key}, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            # بررسی اینکه آیا شماره تلفن و کد ملی تکراری نباشند
            phone_number = serializer.validated_data.get('phone_number')
            national_id = serializer.validated_data.get('national_id')

            if CustomUser.objects.filter(phone_number=phone_number).exists():
                return Response({"error": "این شماره تماس قبلاً ثبت شده است."}, status=status.HTTP_400_BAD_REQUEST)

            if CustomUser.objects.filter(national_id=national_id).exists():
                return Response({"error": "این کد ملی قبلاً ثبت شده است."}, status=status.HTTP_400_BAD_REQUEST)

            # ساخت کاربر
            user = serializer.save()

            # موفقیت‌آمیز بودن ثبت‌نام
            return Response({"message": "ثبت‌نام با موفقیت انجام شد!"}, status=status.HTTP_201_CREATED)

        # اگر داده‌ها معتبر نیستند
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def get(self, request):
        """Retrieve user profile based on phone number."""
        phone_number = request.query_params.get("phone_number")  # Extract phone number from query parameters

        if not phone_number:
            return Response({"error": "شماره تماس ضروری است!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({"error": "کاربری با این شماره تماس پیدا نشد!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateIndividualCaseView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')  # دریافت شماره تماس از درخواست

        try:
            user = CustomUser.objects.get(phone_number=phone_number)  # جستجوی کاربر بر اساس شماره تماس
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # بررسی نوع شخص
        if user.person_type != CustomUser.INDIVIDUAL:
            return Response({"error": "این کاربر نمی‌تواند پرونده حقیقی ایجاد کند."},
                            status=status.HTTP_400_BAD_REQUEST)

        # ایجاد یک کپی از request.data
        data = request.data.copy()

        # اضافه کردن user به داده‌های درخواست
        data['user'] = user.id

        # اعتبارسنجی و ذخیره داده‌ها
        serializer = IndividualCaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateLegalCaseView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')  # دریافت شماره تماس از درخواست

        try:
            user = CustomUser.objects.get(phone_number=phone_number)  # جستجوی کاربر بر اساس شماره تماس
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # بررسی نوع شخص
        if user.person_type != CustomUser.LEGAL:
            return Response({"error": "این کاربر نمی‌تواند پرونده حقوقی ایجاد کند."},
                            status=status.HTTP_400_BAD_REQUEST)

        # بررسی فایل‌های حقیقی
        if (request.data.get('trade_license') or request.data.get('lease_agreement') or
            request.data.get('employer_identification_docs') or request.data.get('other_official_licenses')):
            return Response({"error": "کاربر حقوقی نمی‌تواند فایل‌های حقیقی ارسال کند."}, status=status.HTTP_400_BAD_REQUEST)

        # ایجاد یک کپی از request.data
        data = request.data.copy()

        # اضافه کردن user به داده‌های درخواست
        data['user'] = user.id

        # اعتبارسنجی و ذخیره داده‌ها
        serializer = LegalCaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCasesView(APIView):
    def get(self, request):
        phone_number = request.query_params.get('phone_number')  # دریافت شماره تماس از پارامترهای درخواست

        if not phone_number:
            return Response({"error": "شماره تماس الزامی است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(phone_number=phone_number)  # جستجوی کاربر بر اساس شماره تماس
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # دریافت تمام پرونده‌های حقیقی و حقوقی کاربر
        individual_cases = IndividualCaseView.objects.filter(user=user)
        legal_cases = LegalCaseView.objects.filter(user=user)

        # سریالایز کردن داده‌ها
        individual_serializer = IndividualCaseSerializer(individual_cases, many=True)
        legal_serializer = LegalCaseSerializer(legal_cases, many=True)

        # ترکیب نتایج
        response_data = {
            "individual_cases": individual_serializer.data,
            "legal_cases": legal_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)