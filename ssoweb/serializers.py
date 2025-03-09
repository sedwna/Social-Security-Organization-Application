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
            "id", "first_name","last_name", "person_type", "person_type_display",
            "phone_number", "gender", "gender_display", "province",
            "province_display", "address", "national_id", "birth_date"
        ]



class IndividualCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualCaseView
        fields = '__all__'


class LegalCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalCaseView
        fields = '__all__'
