from django.urls import path
from .views import ChatBotView, get_csrf_token

urlpatterns = [
    path('chat/', ChatBotView.as_view(), name='chat'),
    path('csrf/', get_csrf_token, name='get_csrf_token'),
]