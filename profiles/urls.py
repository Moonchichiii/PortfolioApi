from django.urls import path
from .views import ProfileDetailView

urlpatterns = [
    path('', ProfileDetailView.as_view(), name='profile-list'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
]
