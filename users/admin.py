from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import *  # Import your custom form

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        'mobile', 'name', 'email', 'is_staff', 'is_active', 'verified', 'go_live',
        'gender', 'dob'
    )
    list_filter = ('is_staff', 'is_active', 'verified', 'go_live', 'gender')

    fieldsets = (
        (None, {
            'fields': (
                'mobile', 'password', 'firebase_uid',
                'name', 'email', 'profile_photo', 'user_video', 'aadhaar_card_image',
                'dob', 'gender', 'location', 'marital_status', 'description', 'keywords',
                'occupation_category', 'occupation', 'occupation_subcategory',
                'profession', 'income',
                'facebook', 'instagram', 'linkedin', 'twitter',
                'go_live', 'verified',
            )
        }),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Groups & Permissions', {'fields': ('groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'mobile', 'password1', 'password2', 'name', 'email',
                'is_staff', 'is_active', 'verified', 'go_live'
            ),
        }),
    )

    search_fields = ('mobile', 'name', 'email')
    ordering = ('mobile',)


admin.site.register(User, CustomUserAdmin)