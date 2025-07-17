from django.urls import path

from .views import *

from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static





from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='user-profile')


urlpatterns = [
    path('login-admin/', login_admin, name='login_admin'),
    path('signup/', SignupView.as_view(), name='signup'),
    
    path('reset-password/', ResetPasswordView.as_view(), name='ResetPasswordView'),
    path('logout/', logout_page, name='logout'),

    path('view-user/<user_id>', view_user, name='view_user'),
    path('verified/<user_id>', verified_user, name='verified'),
    path('user_list/', user_list, name='user_list'),
    

] + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
