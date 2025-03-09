from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from rest_framework.exceptions import ValidationError


# Create your models here.


class CustomUser(AbstractUser):
    INDIVIDUAL = 'individual'
    LEGAL = 'legal'

    PERSON_TYPE_CHOICES = [
        (INDIVIDUAL, 'حقیقی'),
        (LEGAL, 'حقوقی'),
    ]

    MALE = 'male'
    FEMALE = 'female'

    GENDER_CHOICES = [
        (MALE, 'مرد'),
        (FEMALE, 'زن'),
    ]

    PROVINCE_CHOICES = [
        ('021', 'تهران'),
        ('061', 'خوزستان'),
        ('077', 'بوشهر'),
        ('031', 'اصفهان'),
        ('051', 'خراسان رضوی'),
        ('071', 'فارس'),
        ('041', 'آذربایجان شرقی'),
        ('011', 'مازندران'),
        ('034', 'کرمان'),
        ('026', 'البرز'),
        ('013', 'گیلان'),
        ('074', 'کهگیلویه و بویراحمد'),
        ('044', 'آذربایجان غربی'),
        ('076', 'هرمزگان'),
        ('086', 'مرکزی'),
        ('035', 'یزد'),
        ('083', 'کرمانشاه'),
        ('028', 'قزوین'),
        ('054', 'سیستان و بلوچستان'),
        ('081', 'همدان'),
        ('084', 'ایلام'),
        ('017', 'گلستان'),
        ('066', 'لرستان'),
        ('024', 'زنجان'),
        ('045', 'اردبیل'),
        ('025', 'قم'),
        ('087', 'کردستان'),
        ('023', 'سمنان'),
        ('038', 'چهارمحال و بختیاری'),
        ('058', 'خراسان شمالی'),
        ('056', 'خراسان جنوبی'),
    ]

    person_type = models.CharField(max_length=10, choices=PERSON_TYPE_CHOICES, verbose_name="نوع شخص")
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره تماس")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name="جنسیت")
    province = models.CharField(max_length=3, choices=PROVINCE_CHOICES, verbose_name="استان محل سکونت")
    address = models.TextField(verbose_name="آدرس دقیق")
    national_id = models.CharField(max_length=10, unique=True, verbose_name="کد ملی")
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')

    def __str__(self):
        return f"{self.username} - {self.phone_number}"




class BaseCase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cases')

    # وضعیت پرونده
    ACCEPT = 'accept'
    REJECT = 'reject'
    DRAFT = 'draft'
    STATUS_CHOICES = [
        (ACCEPT, 'تایید شده'),
        (REJECT, 'رد شده'),
        (DRAFT, 'درحال بررسی'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)

    # شماره پرونده (برای همه‌ی پرونده‌ها)
    case_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    class Meta:
        abstract = True  # این کلاس به صورت انتزاعی است و جدول جداگانه‌ای در پایگاه داده ایجاد نمی‌کند.



class IndividualCaseView(BaseCase):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='individual_cases')  # تغییر related_name

    # فیلدهای مربوط به کاربران حقیقی
    trade_license = models.FileField(upload_to='trade_licenses/', null=True, blank=True)
    lease_agreement = models.FileField(upload_to='lease_agreements/', null=True, blank=True)
    employer_identification_docs = models.FileField(upload_to='employer_identifications/', null=True, blank=True)
    other_official_licenses = models.FileField(upload_to='other_licenses/', null=True, blank=True)

    def __str__(self):
        return f"Individual Case {self.case_number} - {self.user.phone_number}"

class LegalCaseView(BaseCase):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='legal_cases')  # تغییر related_name

    # فیلدهای مربوط به کاربران حقوقی
    operation_license = models.FileField(upload_to='operation_licenses/', null=True, blank=True)
    establishment_license = models.FileField(upload_to='establishment_licenses/', null=True, blank=True)
    articles_of_association = models.FileField(upload_to='articles_of_association/', null=True, blank=True)
    ceo_identification_docs = models.FileField(upload_to='ceo_identifications/', null=True, blank=True)

    def __str__(self):
        return f"Legal Case {self.case_number} - {self.user.phone_number}"

class OTP(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"OTP for {self.phone_number} - Code: {self.code}"

    def is_expired(self):
        """Check if the OTP is expired (valid for 5 minutes)."""
        print(f"Created At (UTC): {self.created_at}")
        print(f"Current Time (UTC): {timezone.now()}")

        return self.created_at < timezone.now() - timedelta(minutes=5)
