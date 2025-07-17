from django import forms
from django.forms import inlineformset_factory
from .models import *


# forms.py

class ScamSocialMediaForm(forms.ModelForm):
    class Meta:
        model = ScamSocialMedia
        fields = ['platform', 'username']
        widgets = {
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }



class ScamComplaintForm(forms.ModelForm):
    class Meta:
        model = ScamComplaint
        fields = [
            'name', 'website', 'company_name', 'phone_number', 'email', 'location',
            'category', 'description', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ScamProofForm(forms.ModelForm):
    class Meta:
        model = ScamProof
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# Inline formset: links ScamProof to ScamComplaint
ScamProofFormSet = inlineformset_factory(
    ScamComplaint, ScamProof,
    form=ScamProofForm,
    extra=1,  # Number of extra blank proof forms shown
    can_delete=False
)



ScamSocialMediaFormSet = inlineformset_factory(
    ScamComplaint, ScamSocialMedia,
    fields=['platform', 'username'],
    form=ScamSocialMediaForm,
    extra=1,
    can_delete=True
)
