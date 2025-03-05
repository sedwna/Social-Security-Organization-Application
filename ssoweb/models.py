from django.db import models
from django.contrib.auth.models import AbstractUser


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

    def __str__(self):
        return f"{self.username} - {self.phone_number}"
