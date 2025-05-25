
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'mobile', 'email', 'dob', 'gender', 'location',
            'marital_status', 'income', 'profession', 'profile_photo'
        ]
        read_only_fields = ['id', 'mobile']