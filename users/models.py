from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        """Create and return a regular user with a mobile number and password."""
        if not mobile:
            raise ValueError("The Mobile field must be set")
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(mobile, password, **extra_fields)


GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

MARITAL_STATUS_CHOICES = [
    ('single', 'Single'),
    ('married', 'Married'),
    ('divorced', 'Divorced'),
    ('widowed', 'Widowed'),
]


from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, EmailValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):

    firebase_uid = models.CharField(max_length=128, unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True)

    # Add these two new fields
    name = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)

    email = models.EmailField(
        null=True,
        blank=True,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )

    # Remove username field
    username = None
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)

    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    profession = models.CharField(max_length=100, null=True, blank=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.mobile
