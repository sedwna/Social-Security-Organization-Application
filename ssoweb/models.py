from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    class Province(models.TextChoices):
        TEHRAN = '021', 'تهران'
        KHUZESTAN = '061', 'خوزستان'
        BUSHEHR = '077', 'بوشهر'
        ESFAHAN = '031', 'اصفهان'
        KHORASAN_RAZAVI = '051', 'خراسان رضوی'
        FARS = '071', 'فارس'
        AZARBAYJAN_EAST = '041', 'آذربایجان شرقی'
        MAZANDARAN = '011', 'مازندران'
        KERMAN = '034', 'کرمان'
        ALBORZ = '026', 'البرز'
        GILAN = '013', 'گیلان'
        KOHKILOUYE_AND_BOYERAHMAD = '074', 'کهگیلویه و بویراحمد'
        AZARBAYJAN_WEST = '044', 'آذربایجان غربی'
        HORMOZGAN = '076', 'هرمزگان'
        MARKAZI = '086', 'مرکزی'
        YAZD = '035', 'یزد'
        TRANSREGIONAL = '000', 'فرامنطقه‌ای'
        KERMANSHAH = '083', 'کرمانشاه'
        QAZVIN = '028', 'قزوین'
        SISTAN_AND_BALUCHESTAN = '054', 'سیستان و بلوچستان'
        HAMEDAN = '081', 'همدان'
        ILAM = '084', 'ایلام'
        GOLESTAN = '017', 'گلستان'
        LORESTAN = '066', 'لرستان'
        ZANJAN = '024', 'زنجان'
        ARDABIL = '045', 'اردبیل'
        QOM = '025', 'قم'
        KORDESTAN = '087', 'کردستان'
        SEMNAN = '023', 'سمنان'
        CHAHARMAHAL_AND_BAKHTIYARI = '038', 'چهارمحال و بختیاری'
        KHORASAN_NORTH = '058', 'خراسان شمالی'
        KHORASAN_SOUTH = '056', 'خراسان جنوبی'

    class Gender(models.TextChoices):
        MALE = 'M', 'آقا'
        FEMALE = 'F', 'خانم'

    class UserType(models.TextChoices):
        REAL = 'R', 'حقیقی'
        LEGAL = 'L', 'حقوقی'

    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    national_code = models.CharField(max_length=11, null=True, blank=True)
    province = models.CharField(max_length=3, choices=Province.choices)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    user_type = models.CharField(max_length=1, choices=UserType.choices, null=True, blank=True)


class File(models.Model):
    # relation
    id_file = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')


class   RealFile(models.Model):
    pass

class LegalFile(models.Model):
    pass

class Workshop(models.Model):
    pass


class Transaction(models.Model):
    pass


class Payment(models.Model):
    pass


class List(models.Model):
    pass

class InsurancePremium(models.Model):
    pass