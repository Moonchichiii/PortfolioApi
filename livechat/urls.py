from django.urls import path
from .views import ChatMessageListCreateView, OnlineUsersListView

urlpatterns = [
    path('<str:room_name>/messages/', ChatMessageListCreateView.as_view(), name='chat-message-list-create'),
    path('online/', OnlineUsersListView.as_view(), name='online-users'),
]
