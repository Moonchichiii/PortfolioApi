import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from profiles.serializers import ProfileSerializer

@pytest.mark.django_db
def test_profile_view(create_user):
    user, profile = create_user('testuser', 'testpassword123')
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(reverse('profile-detail', args=[profile.id]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_profile_creation(create_user):
    user, profile = create_user('testuser', 'testpassword123')
    assert profile.user.username == 'testuser'

@pytest.mark.django_db
def test_profile_str(create_user):
    user, profile = create_user('testuser', 'testpassword123')
    assert str(profile) == f'Profile of {user.username}'

@pytest.mark.django_db
def test_profile_serializer(create_user):
    user, profile = create_user('testuser', 'testpassword123')
    serializer = ProfileSerializer(profile)
    assert serializer.data['user'] == user.id

@pytest.fixture(scope='function', autouse=True)
def clean_up_database(transactional_db):
    pass
