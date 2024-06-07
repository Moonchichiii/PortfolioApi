from django.urls import path
from .views import ProfileDetailView, OnlineUsersListView

urlpatterns = [
    path('', ProfileDetailView.as_view(), name='profile_detail'),
    path('online/', OnlineUsersListView.as_view(), name='online_users'),
]
