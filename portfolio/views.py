"""
This module provides views for the portfolio app.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PortfolioItem
from .serializers import PortfolioItemSerializer

class PortfolioItemListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating portfolio items.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioItemSerializer

    def get_queryset(self):
        # Order the queryset by a specific field, e.g., 'created_at' or 'id'
        return PortfolioItem.objects.filter(profile=self.request.user.profile).order_by('id')

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

class PortfolioItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a portfolio item.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioItemSerializer

    def get_queryset(self):
        # Order the queryset by a specific field, e.g., 'created_at' or 'id'
        return PortfolioItem.objects.filter(profile=self.request.user.profile).order_by('id')
