from rest_framework import serializers
from .models import ScamComplaint, ScamProof


class ScamProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScamProof
        fields = ['id', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']



class ScamComplaintSerializer(serializers.ModelSerializer):
    proofs = ScamProofSerializer(many=True, write_only=True, required=False)
    uploaded_proofs = ScamProofSerializer(many=True, read_only=True, source='proofs')

    class Meta:
        model = ScamComplaint
        fields = '__all__'
        read_only_fields = ['user', 'is_resolved', 'created_at']
    
    def create(self, validated_data):
        proofs_data = validated_data.pop('proofs', [])
        complaint = ScamComplaint.objects.create(**validated_data)
        for proof in proofs_data:
            ScamProof.objects.create(complaint=complaint, **proof)
        return complaint

