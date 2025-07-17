import django_filters
from .models import *

# class couponFilter(django_filters.FilterSet):
#     class Meta:
#         model = coupon
#         exclude = ['image']  # ⛔ Exclude unsupported field

# class home_bannerFilter(django_filters.FilterSet):
#     class Meta:
#         model = home_banner
#         exclude = ['image']  # ⛔ Exclude unsupported field

import django_filters
from .models import ScamComplaint
from django import forms
from users.models import User  # or use get_user_model() if needed
from masters.models import ScamCategory

class ScamComplaintFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Scammer name'})
    )

    phone_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Phone Number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    category = django_filters.ModelChoiceFilter(
        queryset=ScamCategory.objects.all(),
        label='Category',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    status = django_filters.ChoiceFilter(
        choices=ScamComplaint.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Status'
    )

    class Meta:
        model = ScamComplaint
        fields = ['name', 'phone_number', 'email', 'category', 'status']