from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

from .views import JWTLoginView, JWTRegisterView, JWTLogoutView, UserDetailsView, RootView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RootView.as_view(), name='root'),
    path('api/auth/register/', JWTRegisterView.as_view(), name='register'),
    path('api/auth/login/', JWTLoginView.as_view(), name='login'),
    path('api/auth/logout/', JWTLogoutView.as_view(), name='logout'),
    path('api/auth/user/', UserDetailsView.as_view(), name='user_details'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('password_reset/', reset_password_request_token, name='password_reset_request'),
    path('password_reset/confirm/', reset_password_confirm, name='password_reset_confirm'),
    path('api/profiles/', include('profiles.urls')),
    path('api/portfolio/', include('portfolio.urls')),
]
