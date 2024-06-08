from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk'

class OnlineUsersListView(generics.ListAPIView):
    queryset = Profile.objects.filter(is_online=True)
    serializer_class = ProfileSerializer