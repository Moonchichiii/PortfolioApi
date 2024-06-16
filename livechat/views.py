from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, ChatMessage
from rest_framework import generics
from rest_framework import permissions
from profiles.models import Profile
from profiles.serializers import ProfileSerializer

# Create your views here.


@login_required
def chat_room(request, room_name):
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    messages = room.messages.order_by('-timestamp')[:20]  
    return render(request, 'chat/room.html', {'room': room, 'messages': messages})



class OnlineUsersListView(generics.ListAPIView):
    queryset = Profile.objects.filter(is_online=True)
    serializer_class = ProfileSerializer
