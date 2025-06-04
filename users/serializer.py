
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *
from masters.models import *


class OccupationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = occupation_category
        fields = ['id', 'name']

class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = occupation
        fields = ['id', 'name']

class OccupationSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = occupation_subcategory
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
   
   
    occupation_category_detail = OccupationCategorySerializer(read_only=True)
    occupation_category_id = serializers.PrimaryKeyRelatedField(
        source='occupation_category', queryset=occupation_category.objects.all(), write_only=True
    )

    occupation_detail = OccupationSerializer(read_only=True)
    occupation_id = serializers.PrimaryKeyRelatedField(
        source='occupation', queryset=occupation.objects.all(), write_only=True
    )

    occupation_subcategory_detail = OccupationSubcategorySerializer(read_only=True)
    occupation_subcategory_id = serializers.PrimaryKeyRelatedField(
        source='occupation_subcategory', queryset=occupation_subcategory.objects.all(), write_only=True
    )

    keywords = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    keywords_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'mobile', 'is_active', 'name', 'language', 'email', 'dob', 'gender',
            'marital_status', 'location', 'income', 'profession',
            'profile_photo', 'keywords', 'keywords_display',
            'occupation_category_detail', 'occupation_detail', 'occupation_subcategory_detail',
            'occupation_category_id', 'occupation_id', 'occupation_subcategory_id'
        ]
        read_only_fields = ['id', 'mobile']
        extra_kwargs = {
            'is_active': {'required': False},  # optionally
        }

        

    def get_keywords_display(self, obj):
        return obj.keywords.split(",") if obj.keywords else []

    def update(self, instance, validated_data):
        keywords = validated_data.pop("keywords", None)
        if keywords is not None:
            validated_data["keywords"] = ",".join(keywords)
        return super().update(instance, validated_data)