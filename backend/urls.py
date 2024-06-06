from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from .views import JWTLoginView, JWTLogoutView, JWTRegisterView, UserDetailsView
from profiles.views import ProfileDetailView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', JWTRegisterView.as_view(), name='register'),
    path('api/auth/login/', JWTLoginView.as_view(), name='login'),
    path('api/auth/logout/', JWTLogoutView.as_view(), name='logout'),
    path('api/auth/social/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/auth/social/facebook/', FacebookLogin.as_view(), name='facebook_login'),
    path('api/auth/password/reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/auth/password/reset/confirm/', include('dj_rest_auth.urls')),
    path('api/auth/user/', UserDetailsView.as_view(), name='user_details'),  
    path('api/profiles/', ProfileDetailView.as_view(), name='profile_detail'),
    path('api/portfolio/', include('portfolio.urls')),
]

if settings.REST_USE_JWT:
    from rest_framework_simplejwt.views import TokenVerifyView
    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('api/token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    ]
