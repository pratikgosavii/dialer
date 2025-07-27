from rest_framework import viewsets, permissions
from .models import ScamComplaint
from .serializers import ScamComplaintSerializer


from rest_framework import parsers

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class ScamComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ScamComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # ✅ Add this

    def get_queryset(self):
        return ScamComplaint.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render


# Create your views here.


from .models import *
from .forms import *
from .filters import *
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from .serializers import *

from users.permissions import *

from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import ScamComplaint, ScamProof
from .serializers import ScamProofSerializer

class UploadScamProofView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]


    def get(self, request, complaint_id):
        complaint = ScamComplaint.objects.filter(id=complaint_id, user=request.user).first()
        if not complaint:
            return Response({'error': 'Complaint not found'}, status=404)

        proofs = complaint.proofs.all()
        serializer = ScamProofSerializer(proofs, many=True)
        return Response(serializer.data)

    def post(self, request, complaint_id):
        complaint = ScamComplaint.objects.filter(id=complaint_id, user=request.user).first()
        if not complaint:
            return Response({'error': 'Complaint not found'}, status=404)

        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=400)

        proof = ScamProof.objects.create(complaint=complaint, file=file)
        return Response(ScamProofSerializer(proof).data)





def add_complaint(request):
    
    if request.method == 'POST':
        complaint_form = ScamComplaintForm(request.POST)
        proof_formset = ScamProofFormSet(request.POST, request.FILES)

        if complaint_form.is_valid() and proof_formset.is_valid():
            complaint = complaint_form.save(commit=False)
            complaint.user = request.user
            complaint.save()

            # link formset to the saved complaint instance
            proof_formset.instance = complaint
            proof_formset.save()

            return redirect('list_complaint')  # change to your success URL
        else:

            print(complaint_form.errors)
    else:
        complaint_form = ScamComplaintForm()
        proof_formset = ScamProofFormSet()

    return render(request, 'add_complaint.html', {
        'complaint_form': complaint_form,
        'proof_formset': proof_formset,
    })

def update_complaint(request, complaint_id):
    
    complaint = get_object_or_404(ScamComplaint, pk=complaint_id)

    if request.method == 'POST':
        complaint_form = ScamComplaintForm(request.POST, instance=complaint)
        proof_formset = ScamProofFormSet(request.POST, request.FILES, instance=complaint, prefix='proofs')
        social_formset = ScamSocialMediaFormSet(request.POST, instance=complaint, prefix='socials')

        if complaint_form.is_valid() and proof_formset.is_valid() and social_formset.is_valid():
            complaint = complaint_form.save()
            proof_formset.save()
            social_formset.save()
            return redirect('list_complaint')  # ✅ your desired success page
    else:
        complaint_form = ScamComplaintForm(instance=complaint)
        proof_formset = ScamProofFormSet(instance=complaint, prefix='proofs')
        social_formset = ScamSocialMediaFormSet(instance=complaint, prefix='socials')

    return render(request, 'add_complaint.html', {
        'complaint_form': complaint_form,
        'proof_formset': proof_formset,
        'social_formset': social_formset,
        'update': True,
    })


def delete_social(request, social_id):
    social = get_object_or_404(ScamSocialMedia, id=social_id)
    complaint_id = social.complaint.id
    social.delete()
    return redirect('update_complaint', complaint_id=complaint_id)


def list_complaint(request):

    data = ScamComplaintFilter(request.GET, queryset=ScamComplaint.objects.all())



    return render(request, 'list_complaint.html', {'data' : data.qs, 'filter': ScamComplaintFilter,})


def delete_complaint(request, complaint_id):

    data = ScamComplaint.objects.get(id = complaint_id).delete()

    return redirect('list_complaint')




@login_required
def delete_proof(request, pk):

    proof = get_object_or_404(ScamProof, pk=pk, complaint__user=request.user)
    complaint_id = proof.complaint.id

    # Delete file and entry
    proof.file.delete()
    proof.delete()

    # Redirect using reverse and URL name
    return redirect(reverse('update_complaint', kwargs={'complaint_id': complaint_id}))




from rest_framework import status
from django.db.models import Q
from .models import User
from users.serializer import UserProfileSerializer

class SearchUserView(APIView):
    permission_classes = [IsAuthenticated]  # Optional: remove if public

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(
            Q(go_live=True) & (
                Q(mobile__icontains=query) |
                Q(name__icontains=query) |
                Q(profession__icontains=query)
            )
        ).only('id', 'name', 'mobile', 'profile_photo')[:20]


        serialized_users = UserProfileSerializer(users, many=True)
        return Response(serialized_users.data)
    


# views.py
from stream_chat import StreamChat
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import os


from .utils import generate_channel_id


    
class get_chat_token(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        api_key = os.getenv("STREAM_API_KEY")
        api_secret = os.getenv("STREAM_API_SECRET")

        print("✅ STREAM_API_KEY from .env:", os.getenv("STREAM_API_KEY"))

        print(api_key)
        print(api_secret)

        if not api_key or not api_secret:
            return Response({"error": "Missing Stream credentials"}, status=500)

        user_id = str(request.user.id)

        other_user_id = request.data.get("other_user_id")

        # Generate consistent channel ID
        channel_id = generate_channel_id(user_id, other_user_id)

        # Initialize Stream client
        client = StreamChat(api_key=api_key, api_secret=api_secret)

        # Upsert both users
      
        client.upsert_user({
            "id": str(user_id),
            "name": request.user.get_full_name() or request.user.username,
        })

        client.upsert_user({
            "id": str(other_user_id),
            "name": request.user.get_full_name() or request.user.username,
        })


        # Create token for authenticated user
        token = client.create_token(user_id)

        return Response({
            "user_id": user_id,
            "other_user_id": other_user_id,
            "token": token,
            "channel_id": channel_id,
            "api_key": api_key,  # for frontend use
        })

