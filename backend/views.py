from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login as django_login, logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.serializers import UserDetailsSerializer
from .serializers import LoginSerializer, JWTSerializer, CustomRegisterSerializer, UserDetailsSerializer

User = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password', 'old_password', 'new_password1', 'new_password2')
)

class JWTLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            django_login(request, user)

            response_data = {
                'user': UserDetailsSerializer(user).data,
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
            response = Response(JWTSerializer(response_data).data, status=status.HTTP_200_OK)
            response.set_cookie(settings.JWT_AUTH_COOKIE, access_token, httponly=True, secure=settings.JWT_AUTH_COOKIE_SECURE, samesite='Lax')
            response.set_cookie(settings.JWT_REFRESH_AUTH_COOKIE, refresh_token, httponly=True, secure=settings.JWT_AUTH_COOKIE_SECURE, samesite='Lax')
            return response
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class JWTRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        if settings.REST_SESSION_LOGIN:
            django_login(request, user)

        response_data = {
            'user': UserDetailsSerializer(user).data,
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        response = Response(JWTSerializer(response_data).data, status=status.HTTP_201_CREATED)
        response.set_cookie(settings.JWT_AUTH_COOKIE, access_token, httponly=True, secure=settings.JWT_AUTH_COOKIE_SECURE, samesite='Lax')
        response.set_cookie(settings.JWT_REFRESH_AUTH_COOKIE, refresh_token, httponly=True, secure=settings.JWT_AUTH_COOKIE_SECURE, samesite='Lax')

        return response

class JWTLogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        if settings.REST_SESSION_LOGIN:
            django_logout(request)

        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

        if settings.REST_USE_JWT:
            response.delete_cookie(settings.JWT_AUTH_COOKIE)
            response.delete_cookie(settings.JWT_REFRESH_AUTH_COOKIE)

        return response

class UserDetailsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDetailsSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
