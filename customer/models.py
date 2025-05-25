from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ScamComplaint(models.Model):
    CATEGORY_CHOICES = [
        ('phishing', 'Phishing'),
        ('investment', 'Investment Scam'),
        ('fake_product', 'Fake Product'),
        ('job_fraud', 'Job Fraud'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="scam_complaints")
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()

    social_media_links = models.TextField(
        help_text="Comma-separated links/IDs for Facebook, Instagram, etc.", blank=True, null=True)

    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ScamProof(models.Model):
    complaint = models.ForeignKey(ScamComplaint, on_delete=models.CASCADE, related_name='proofs')
    file = models.FileField(upload_to='scam_proofs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
