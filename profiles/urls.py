from django.urls import path
from .views import ProfileDetailView, OnlineUsersListView

urlpatterns = [
    path('profiles/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/online/', OnlineUsersListView.as_view(), name='online-users'),
]
