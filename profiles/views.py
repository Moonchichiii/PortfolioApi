from rest_framework import generics
from rest_framework import permissions
from .models import Profile
from .serializers import ProfileSerializer

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk'

class ProfileMeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

class OnlineUsersListView(generics.ListAPIView):
    queryset = Profile.objects.filter(is_online=True)
    serializer_class = ProfileSerializer