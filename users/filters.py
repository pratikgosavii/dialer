import django_filters
from django import forms
from .models import User

class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    mobile = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Mobile",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Email",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gender = django_filters.ChoiceFilter(
        choices=User._meta.get_field('gender').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    marital_status = django_filters.ChoiceFilter(
        choices=User._meta.get_field('marital_status').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    language = django_filters.ChoiceFilter(
        choices=User._meta.get_field('language').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    verified = django_filters.BooleanFilter(
        widget=forms.Select(choices=[('', '----'), (True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'})
    )
    go_live = django_filters.BooleanFilter(
        widget=forms.Select(choices=[('', '----'), (True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = [
            'name', 'mobile', 'email', 'gender', 'marital_status',
            'language', 'verified', 'go_live'
        ]
