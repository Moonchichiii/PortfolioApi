from django.urls import path
from .views import ProfileDetailView

urlpatterns = [
    path('profiles/', ProfileDetailView.as_view(), name='profile-detail'),
]