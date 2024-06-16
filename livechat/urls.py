from django.urls import path
from .views import chat_room, OnlineUsersListView

urlpatterns = [
    path('<str:room_name>/', chat_room, name='chat_room'),
    path('online/', OnlineUsersListView.as_view(), name='online-users'),
]
