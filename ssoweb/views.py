import random
from .models import OTP
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import *

# Create your views here.


class SendOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")

        if not phone_number:
            return Response({"error": "شماره تماس ضروری است!"}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی وجود شماره تلفن در سیستم
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({"error": "این شماره تماس در سیستم ثبت نشده است."}, status=status.HTTP_400_BAD_REQUEST)

        # تولید کد OTP
        otp_code = str(random.randint(100000, 999999))

        # ذخیره OTP در دیتابیس
        otp, created = OTP.objects.get_or_create(phone_number=phone_number)
        otp.code = otp_code
        otp.is_valid = True
        otp.save()

        return Response({"message": f"کد تایید {otp_code} به شماره {phone_number} ارسال شد."}, status=status.HTTP_200_OK)




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

        if otp.is_expired():
            return Response({"error": "کد تایید منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)

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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer  # فرض کنید یک Serializer برای CustomUser دارید

class UserProfileView(APIView):
    def get(self, request):
        phone_number = request.query_params.get("phone_number")  # شماره تماس از پارامترهای URL دریافت می‌شود

        if not phone_number:
            return Response({"error": "شماره تماس ضروری است!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({"error": "کاربری با این شماره تماس پیدا نشد!"}, status=status.HTTP_404_NOT_FOUND)

        # استفاده از Serializer برای تبدیل مدل به داده قابل نمایش
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)






class CreateCaseView(APIView):
    def post(self, request):
        serializer = CaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUserCasesView(APIView):
    def get(self, request):
        cases = Case.objects.filter(user=request.user)
        serializer = CaseSerializer(cases, many=True)
        return Response(serializer.data)



class CreateWorkshopView(APIView):
    def post(self, request):
        # دریافت داده‌ها از درخواست
        case_number = request.data.get('case_number')
        workshop_code = request.data.get('workshop_code')
        period = request.data.get('period')
        status = request.data.get('status')
        activity_type = request.data.get('activity_type')
        activity_start_date = request.data.get('activity_start_date')

        # بررسی وجود پرونده با این شماره پرونده
        try:
            case = Case.objects.get(case_number=case_number)
        except Case.DoesNotExist:
            return Response({"error": "شماره پرونده پیدا نشد."}, status=status.HTTP_400_BAD_REQUEST)

        # ایجاد کارگاه جدید
        workshop = Workshop.objects.create(
            case=case,
            workshop_code=workshop_code,
            period=period,
            status=status,
            activity_type=activity_type,
            activity_start_date=activity_start_date
        )

        # بازگشت پاسخ موفقیت‌آمیز
        serializer = WorkshopSerializer(workshop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ListUserWorkshopsView(APIView):
    def get(self, request):
        # دریافت شماره پرونده کاربر
        user = request.user  # فرض می‌کنیم که کاربر احراز هویت شده است
        case_number = user.case.case_number  # فرض می‌کنیم که هر کاربر فقط یک پرونده دارد

        # فیلتر کارگاه‌ها بر اساس شماره پرونده کاربر
        workshops = Workshop.objects.filter(case__case_number=case_number)

        # استفاده از Serializer برای تبدیل داده‌ها به فرمت JSON
        serializer = WorkshopSerializer(workshops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

