from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'email', 'bio', 'avatar', 'location', 'is_online']