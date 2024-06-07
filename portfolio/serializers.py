from rest_framework import serializers
from .models import PortfolioItem

class PortfolioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        fields = ['id', 'profile', 'title', 'description', 'created_at', 'updated_at']
        read_only_fields = ['profile']
