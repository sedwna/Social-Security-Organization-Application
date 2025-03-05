from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import OTP


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

@admin.register(IndividualCaseView)
class IndividualCaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'user', 'status' )
    list_filter = ('status', 'user__person_type')
    search_fields = ('case_number', 'user__phone_number')

@admin.register(LegalCaseView)
class LegalCaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'user', 'status')
    list_filter = ('status', 'user__person_type')
    search_fields = ('case_number', 'user__phone_number')
