from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer

# Create your views here.


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile
