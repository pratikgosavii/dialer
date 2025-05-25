from rest_framework.routers import DefaultRouter
from .views import ScamComplaintViewSet, UploadScamProofView
from django.urls import path

router = DefaultRouter()
router.register('scam', ScamComplaintViewSet, basename='scam')

urlpatterns = router.urls + [
    path('scams/upload-proof/<int:complaint_id>', UploadScamProofView.as_view(), name='upload-scam-proof'),
]
