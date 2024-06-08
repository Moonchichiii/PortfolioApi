import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from profiles.models import Profile

@pytest.mark.django_db
def test_get_profile(create_user):
    user, profile = create_user('testuser', 'testpassword123')
    client = APIClient()
    client.force_authenticate(user=user)
    
    response = client.get(reverse('profile-detail', args=[profile.id]))
    assert response.status_code == 200
    assert 'id' in response.data

@pytest.mark.django_db
def test_update_profile(create_user):
    user, profile = create_user('testuser', 'testpassword123')
    client = APIClient()
    client.force_authenticate(user=user)
    
    data = {'bio': 'New bio', 'user': user.id} 
    response = client.put(reverse('profile-detail', args=[profile.id]), data, format='json')
    assert response.status_code == 200
    assert response.data['bio'] == 'New bio'

@pytest.fixture(scope='function', autouse=True)
def clean_up_database(transactional_db):
    pass
