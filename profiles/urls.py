from django.urls import path
from .views import ProfileDetailView, ProfileMeView

urlpatterns = [
    path('', ProfileDetailView.as_view(), name='profile-list'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('me/', ProfileMeView.as_view(), name='profile-me'),
]
