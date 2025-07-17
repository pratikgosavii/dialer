from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .forms import *


# def login_page(request):
#     forms = LoginForm()
#     if request.method == 'POST':
#         forms = LoginForm(request.POST)
#         if forms.is_valid():
#             username = forms.cleaned_data['username']
#             password = forms.cleaned_data['password']
#             print(username)
#             print(password)
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)

#                 if user.is_doctor:
#                     print('---------------------------------')
#                     print('---------------------------------')
#                     print('---------------------------------')
#                 return redirect('dashboard')
#             else:
#                 messages.error(request, 'wrong username password')
#     context = {'form': forms}
#     return render(request, 'adminLogin.html', context)

from firebase_admin import auth as firebase_auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User  # Your custom user model


class SignupView(APIView):
    def post(self, request):
        id_token = request.data.get("idToken")
        if not id_token:
            return Response({"error": "idToken is required"}, status=400)

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            mobile = decoded_token.get("phone_number")
            uid = decoded_token.get("uid")

            if not mobile:
                return Response({"error": "Phone number not found in token"}, status=400)

            user = User.objects.filter(mobile=mobile).first()
            created = False

            if user:
                # Update UID if changed
                if user.firebase_uid != uid:
                    user.firebase_uid = uid
                    user.save()
            else:
                # Create new user
                user = User.objects.create(
                    mobile=mobile,
                    firebase_uid=uid
                )
                created = True

            # Optional: handle extra profile fields sent from frontend
            optional_fields = [
                "email", "dob", "gender", "location", "marital_status",
                "income", "profession", "profile_photo"
            ]
            for field in optional_fields:
                if field in request.data:
                    setattr(user, field, request.data.get(field))

            user.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "mobile": user.mobile,
                    "created": created,
                }
            })

        except Exception as e:
            return Response({"error": "Invalid or expired Firebase token."}, status=400)






from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .serializer import UserProfileSerializer
from .models import User
from rest_framework.decorators import action


class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'put'], url_path='me')
    def me(self, request):
        user = request.user

        if request.method == 'GET':
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from .permissions import *


class ResetPasswordView(APIView):
    def post(self, request):
        id_token = request.data.get("idToken")
        new_password = request.data.get("new_password")

        if not id_token or not new_password:
            return Response({"error": "idToken and new_password are required"}, status=400)

        try:
            # Decode the token to get UID
            decoded = firebase_auth.verify_id_token(id_token)
            uid = decoded.get("uid")

            # Update Firebase password
            firebase_auth.update_user(uid, password=new_password)

            return Response({"message": "Password updated successfully."})

        except Exception as e:
            return Response({"error": str(e)}, status=400)
        



def login_admin(request):

    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            mobile = forms.cleaned_data['mobile']
            password = forms.cleaned_data['password']
            print(mobile)
            print(password)
            user = authenticate(mobile=mobile, password=password)
            if user:
                login(request, user)

                if user.is_superuser:
                    print('---------------------------------')
                    print('---------------------------------')
                    print('---------------------------------')
                return redirect('dashboard')
            else:
                messages.error(request, 'wrong username password')
    context = {'form': forms}
    return render(request, 'adminLogin.html', context)

def logout_page(request):
    logout(request)
    return redirect('login_admin')

def customer_user_list(request):

    data = User.objects.all()

    return render(request, 'user_list.html', { 'data' : data})


def view_user(request, user_id):

    data = User.objects.get(id = user_id)

    return render(request, 'view_user.html', { 'data' : data})


def verified_user(request, user_id):

    data = User.objects.get(id = user_id)
    data.verified = True
    data.save()

    return redirect('view_user', user_id=data.id)




def user_list(request):

    data = User.objects.all()

    return render(request, 'user_list.html', { 'data' : data})
