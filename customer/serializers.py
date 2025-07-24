from rest_framework import serializers
from .models import *


class ScamProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScamProof
        fields = ['id', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']






class ScamSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScamSocialMedia
        fields = ['platform', 'username']


import json

class ScamComplaintSerializer(serializers.ModelSerializer):
    proofs = ScamProofSerializer(many=True, write_only=True, required=False)
    uploaded_proofs = ScamProofSerializer(many=True, read_only=True, source='proofs')

    socials = ScamSocialMediaSerializer(many=True, required=False)
    uploaded_socials = ScamSocialMediaSerializer(many=True, read_only=True, source='socials')


    class Meta:
        model = ScamComplaint
        fields = '__all__'
        read_only_fields = ['user', 'is_resolved', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        
        # Handle stringified JSON for 'socials' in form-data
        socials_data = request.data.get('socials')
        if socials_data and isinstance(socials_data, str):
            try:
                socials_data = json.loads(socials_data)
            except json.JSONDecodeError:
                raise serializers.ValidationError({"socials": "Invalid JSON format."})
        else:
            socials_data = validated_data.pop('socials', [])

        proofs_data = validated_data.pop('proofs', [])

        complaint = ScamComplaint.objects.create(**validated_data)

        for proof in proofs_data:
            ScamProof.objects.create(complaint=complaint, **proof)

        for social in socials_data:
            ScamSocialMedia.objects.create(complaint=complaint, **social)

        return complaint