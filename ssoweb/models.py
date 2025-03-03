from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Person(models.Model):
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

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_code = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField()
    address = models.TextField(max_length=300)
    slug = models.SlugField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    province = models.CharField(max_length=3,choices=Province.choices,default=None)


    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['-created_at']),
        ]
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class File(models.Model):
    person = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,related_name='userFiles')

#
#
# class RealFile(models.Model):
#
#     person = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,related_name='user-files')
#
#
#
# class LegalFile(models.Model):
#     person = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,related_name='user-files')

