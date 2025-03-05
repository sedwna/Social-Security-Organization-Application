from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import OTP
from django.utils.timezone import now


# مدل کاربران
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'phone_number', 'person_type', 'gender', 'national_id')
    search_fields = ('username', 'phone_number', 'national_id')
    list_filter = ('person_type', 'gender', 'province')

    fieldsets = (
        (None, {
            'fields': (
                'person_type', 'username', 'phone_number', 'password', 'gender', 'province', 'address', 'national_id',
                'birth_date',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'phone_number', 'password')
        }),
    )

    def save_model(self, request, obj, form, change):
        # بررسی که آیا شماره تلفن یا کد ملی تکراری نباشند
        if CustomUser.objects.filter(phone_number=obj.phone_number).exclude(id=obj.id).exists():
            raise ValidationError("این شماره تماس قبلاً ثبت شده است.")
        if CustomUser.objects.filter(national_id=obj.national_id).exclude(id=obj.id).exists():
            raise ValidationError("این کد ملی قبلاً ثبت شده است.")
        super().save_model(request, obj, form, change)


# مدل پرونده‌ها
@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'case_number', 'person_type', 'trade_license', 'operation_license')
    search_fields = ('case_number', 'user__username', 'user__phone_number')
    list_filter = ('person_type', 'user__person_type')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # وقتی که در حال ویرایش یک پرونده هستیم
            if obj.user.person_type == CustomUser.INDIVIDUAL:
                return (
                    'operation_license', 'establishment_license', 'articles_of_association', 'ceo_identification_docs')
            if obj.user.person_type == CustomUser.LEGAL:
                return ('trade_license', 'lease_agreement', 'employer_identification_docs', 'other_official_licenses')
        return super().get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change):
        """در هنگام ذخیره، نوع پرونده را با نوع شخص تطبیق می‌دهد."""
        if obj.user.person_type == CustomUser.INDIVIDUAL:
            if obj.operation_license or obj.establishment_license or obj.articles_of_association or obj.ceo_identification_docs:
                raise ValidationError("کاربر حقیقی نمی‌تواند پرونده حقوقی ایجاد کند.")
        elif obj.user.person_type == CustomUser.LEGAL:
            if obj.trade_license or obj.lease_agreement or obj.employer_identification_docs or obj.other_official_licenses:
                raise ValidationError("کاربر حقوقی نمی‌تواند پرونده حقیقی ایجاد کند.")
        super().save_model(request, obj, form, change)



@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created_at', 'is_valid', 'is_expired')  # نمایش فیلدها در لیست
    list_filter = ('is_valid', 'created_at')  # فیلتر بر اساس وضعیت اعتبار و تاریخ ایجاد
    search_fields = ('phone_number', 'code')  # جستجو بر اساس شماره تلفن و کد

    def is_expired(self, obj):
        """مقدار true یا false برای انقضای OTP"""
        return obj.is_expired()
    is_expired.boolean = True  # برای اینکه به‌صورت یک آیکون Boolean در بیاید
    is_expired.short_description = 'Expired'  # عنوان ستون نمایش داده شده


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('workshop_code', 'case', 'period', 'created_at', 'status', 'activity_type', 'activity_start_date')
    list_filter = ('status', 'period', 'activity_type')
    search_fields = ('workshop_code', 'case__case_number')
