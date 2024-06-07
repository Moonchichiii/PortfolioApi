from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login as django_login, logout as django_logout
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserDetailsSerializer, JWTSerializer


User = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password', 'old_password', 'new_password1', 'new_password2')
)

class JWTLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.debug("Login request received with data: %s", request.data)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            logger.error("Serializer validation failed: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            logger.debug("User authenticated successfully: %s", user)
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
        
        logger.error("Invalid credentials provided for user: %s", request.data.get('username'))
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class JWTRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        django_login(request, user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response_data = {
            'user': UserDetailsSerializer(user).data,
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

        response = Response(response_data, status=status.HTTP_201_CREATED)
        response.set_cookie(settings.JWT_AUTH_COOKIE, access_token, httponly=True, secure=settings.JWT_AUTH_COOKIE_SECURE, samesite='Lax')
        response.set_cookie(settings.JWT_REFRESH_AUTH_COOKIE, refresh_token, httponly=True, secure=settings.JWT_AUTH_COOKIE_SECURE, samesite='Lax')
        return response

class JWTLogoutView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        django_logout(request)
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.JWT_AUTH_COOKIE)
        response.delete_cookie(settings.JWT_REFRESH_AUTH_COOKIE)
        return response

class UserDetailsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDetailsSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
