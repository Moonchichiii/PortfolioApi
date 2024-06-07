from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from .views import JWTLoginView, JWTRegisterView, JWTLogoutView, UserDetailsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', JWTRegisterView.as_view(), name='register'),
    path('api/auth/login/', JWTLoginView.as_view(), name='login'),
    path('api/auth/logout/', JWTLogoutView.as_view(), name='logout'),
    path('api/auth/user/', UserDetailsView.as_view(), name='user_details'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profiles/', include('profiles.urls')),
    path('api/portfolio/', include('portfolio.urls')),
]
