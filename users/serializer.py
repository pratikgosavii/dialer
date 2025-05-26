
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'mobile', 'name', 'language', 'email', 'dob', 'gender',
            'marital_status', 'location', 'income', 'profession', 'profile_photo'
        ]
        read_only_fields = ['id', 'mobile']