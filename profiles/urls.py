from django.urls import path
from .views import ProfileDetailView, OnlineUsersListView

urlpatterns = [
    path('', ProfileDetailView.as_view(), name='profile-list'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('online/', OnlineUsersListView.as_view(), name='online-users'),
]