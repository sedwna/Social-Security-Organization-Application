from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'phone_number', 'first_name', 'last_name','user_type')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional information',{'fields':('date_of_birth', 'national_code','province','gender','phone_number','user_type')}),
    )