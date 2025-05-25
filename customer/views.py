from rest_framework import viewsets, permissions
from .models import ScamComplaint
from .serializers import ScamComplaintSerializer

class ScamComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ScamComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ScamComplaint.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import ScamComplaint, ScamProof
from .serializers import ScamProofSerializer

class UploadScamProofView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, complaint_id):
        complaint = ScamComplaint.objects.filter(id=complaint_id, user=request.user).first()
        if not complaint:
            return Response({'error': 'Complaint not found'}, status=404)

        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=400)

        proof = ScamProof.objects.create(complaint=complaint, file=file)
        return Response(ScamProofSerializer(proof).data)
