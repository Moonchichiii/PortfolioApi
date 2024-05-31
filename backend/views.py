from django.conf import settings
from django.contrib.auth import login as django_login, logout as django_logout, get_backends
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import RegisterView
from .serializers import LoginSerializer, JWTSerializer, CustomRegisterSerializer, UserDetailsSerializer

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password', 'old_password', 'new_password1', 'new_password2')
)


class JWTLoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def login(self):
        self.user = self.serializer.validated_data['user']
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.refresh_token = str(refresh)

        if settings.REST_SESSION_LOGIN:
            self.process_login()

    def get_response(self):
        data = {
            'user': self.user,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token
        }
        serializer = JWTSerializer(instance=data)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response.set_cookie(settings.JWT_AUTH_COOKIE, self.access_token, httponly=True, secure=settings.JWT_AUTH_COOKIE_SECURE, samesite='Lax')
        response.set_cookie(settings.JWT_REFRESH_AUTH_COOKIE, self.refresh_token, httponly=True, secure=settings.JWT_AUTH_COOKIE_SECURE, samesite='Lax')
        return response

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()

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
            backend = get_backends()[0]  
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            django_login(request, user, backend=user.backend)

        user_data = UserDetailsSerializer(user).data

        response = Response({
            'user': user_data,
            'access_token': access_token,
            'refresh_token': refresh_token,
        }, status=status.HTTP_201_CREATED)

        response.set_cookie(settings.JWT_AUTH_COOKIE, access_token, httponly=True, secure=settings.JWT_AUTH_COOKIE_SECURE, samesite='Lax')
        response.set_cookie(settings.JWT_REFRESH_AUTH_COOKIE, refresh_token, httponly=True, secure=settings.JWT_AUTH_COOKIE_SECURE, samesite='Lax')

        return response

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user

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
