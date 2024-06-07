from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PortfolioItem
from .serializers import PortfolioItemSerializer

class PortfolioItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioItemSerializer

    def get_queryset(self):
        return PortfolioItem.objects.filter(profile=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

class PortfolioItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioItemSerializer

    def get_queryset(self):
        return PortfolioItem.objects.filter(profile=self.request.user.profile)
