import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db(transaction=True)
def test_register_view():
    client = APIClient()
    url = reverse('register')
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert 'access_token' in response.data

@pytest.mark.django_db(transaction=True)
def test_login_view(create_user):
    user, profile = create_user('testuser', 'testpassword123')
    client = APIClient()
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'testpassword123'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 200
    assert 'access_token' in response.data

@pytest.mark.django_db(transaction=True)
def test_logout_view(create_user):
    user, profile = create_user('testuser', 'testpassword123')
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('logout')
    response = client.post(url)
    assert response.status_code == 200
    assert response.data['detail'] == 'Successfully logged out.'

@pytest.fixture(scope='function', autouse=True)
def clean_up_database(transactional_db):
    pass