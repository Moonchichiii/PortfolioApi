from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

class OnlineUsersListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(profile__is_online=True)
