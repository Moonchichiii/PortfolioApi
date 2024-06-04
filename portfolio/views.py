from rest_framework import generics, permissions
from .models import PortfolioItem
from .serializers import PortfolioItemSerializer

# Create your views here.

class PortfolioItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PortfolioItemSerializer

    def get_queryset(self):
        return PortfolioItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PortfolioItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PortfolioItemSerializer

    def get_queryset(self):
        return PortfolioItem.objects.filter(user=self.request.user)
