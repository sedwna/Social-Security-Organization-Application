from django.db import models
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from .models import CustomUser


from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    person_type_display = serializers.CharField(source="get_person_type_display", read_only=True)
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)
    province_display = serializers.CharField(source="get_province_display", read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "person_type", "person_type_display",
            "phone_number", "gender", "gender_display", "province",
            "province_display", "address", "national_id", "birth_date"
        ]



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
