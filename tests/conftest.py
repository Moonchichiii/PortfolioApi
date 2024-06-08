import pytest
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()

@pytest.fixture
def create_user():
    def _create_user(username, password):
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
        profile, _ = Profile.objects.get_or_create(user=user)
        return user, profile
    return _create_user