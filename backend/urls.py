from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from .views import JWTLoginView, JWTLogoutView, JWTRegisterView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/login/', JWTLoginView.as_view(), name='login'),
    path('dj-rest-auth/logout/', JWTLogoutView.as_view(), name='logout'),
    path('dj-rest-auth/registration/', JWTRegisterView.as_view(), name='register'),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('dj-rest-auth/password/reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('dj-rest-auth/password/reset/confirm/', include('dj_rest_auth.urls')),
]

if settings.REST_USE_JWT:
    from rest_framework_simplejwt.views import TokenVerifyView
    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    ]
