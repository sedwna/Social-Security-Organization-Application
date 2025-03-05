from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import OTP
# Register your models here.


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created_at')
    search_fields = ('phone_number',)

