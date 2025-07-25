
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *
from masters.models import *
from masters.serializers import *

from customer.serializers import ScamComplaintSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    
    scam_complaints_marked = serializers.SerializerMethodField()

    occupation_category_detail = OccupationCategorySerializer(source='occupation_category', read_only=True)
    occupation_category = serializers.PrimaryKeyRelatedField(
        queryset=occupation_category.objects.all(), required=False
    )

    occupation_detail = OccupationSerializer(source='occupation', read_only=True)
    occupation = serializers.PrimaryKeyRelatedField(
        queryset=occupation.objects.all(), required=False
    )

    occupation_subcategory_detail = OccupationSubcategorySerializer(source='occupation_subcategory', read_only=True)
    occupation_subcategory = serializers.PrimaryKeyRelatedField(
        queryset=occupation_subcategory.objects.all(), required=False
    )

    keywords = serializers.ListField(
        child=serializers.CharField(), required=False, write_only=True
    )
    keywords_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'mobile', 'is_active', 'name', 'language', 'email', 'dob', 'gender', 
            'marital_status', 'location', 'income', 'profession', 'user_video', 'aadhaar_card_image',
            'go_live', 'profile_photo', 'keywords', 'keywords_display', 'description',
            'occupation_category', 'occupation', 'occupation_subcategory',
            'occupation_category_detail', 'occupation_detail', 'occupation_subcategory_detail', 'scam_complaints_marked'
        ]
        read_only_fields = [
            'id', 'mobile', 'occupation_category_detail',
            'occupation_detail', 'occupation_subcategory_detail'
        ]
        extra_kwargs = {
            'is_active': {'required': False},
        }

    def get_keywords_display(self, obj):
        return obj.keywords.split(",") if obj.keywords else []

    def update(self, instance, validated_data):
        keywords = validated_data.pop("keywords", None)
        if keywords is not None:
            validated_data["keywords"] = ",".join(keywords)
        return super().update(instance, validated_data)
    
    def get_scam_complaints_marked(self, obj):
        complaints = obj.scam_complaints.filter(status='mark_as_scam')
        return ScamComplaintSerializer(complaints, many=True).data
