from rest_framework import generics, permissions
from .models import ChatMessage, ChatRoom
from .serializers import ChatMessageSerializer
from profiles.models import Profile
from profiles.serializers import ProfileSerializer

class ChatMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        return ChatMessage.objects.filter(room__name=room_name).order_by('-timestamp')

    def perform_create(self, serializer):
        room_name = self.kwargs['room_name']
        room, created = ChatRoom.objects.get_or_create(name=room_name)
        serializer.save(user=self.request.user, room=room)

class OnlineUsersListView(generics.ListAPIView):
    queryset = Profile.objects.filter(is_online=True)
    serializer_class = ProfileSerializer
