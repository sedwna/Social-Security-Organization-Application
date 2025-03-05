from django.db import models
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from .models import CustomUser


from rest_framework import serializers
from .models import *




class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'gender', 'province', 'address', 'national_id', 'birth_date', 'person_type']


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

    def validate(self, data):
        # تطابق نوع پرونده با نوع شخص
        user = self.context['request'].user
        if user.person_type == CustomUser.INDIVIDUAL and 'operation_license' in data:
            raise serializers.ValidationError("کاربر حقیقی نمی‌تواند پرونده حقوقی ایجاد کند.")
        if user.person_type == CustomUser.LEGAL and 'trade_license' in data:
            raise serializers.ValidationError("کاربر حقوقی نمی‌تواند پرونده حقیقی ایجاد کند.")
        return data



class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ['workshop_code', 'case', 'period', 'created_at', 'status', 'activity_type', 'activity_start_date']
