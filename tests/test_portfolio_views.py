import pytest
from rest_framework.test import APIClient
from portfolio.models import PortfolioItem

@pytest.mark.django_db
def test_portfolio_item_list_create_view(create_user):
    user, profile = create_user('testuser1', 'testpassword123')
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post('/api/portfolio/', {'title': 'Test Portfolio Item', 'description': 'Description'})
    assert response.status_code == 201
    assert PortfolioItem.objects.count() == 1

@pytest.mark.django_db
def test_portfolio_item_detail_view(create_user):
    user, profile = create_user('testuser2', 'testpassword123')
    client = APIClient()
    client.force_authenticate(user=user)

    portfolio_item = PortfolioItem.objects.create(profile=profile, title='Test Portfolio Item', description='Description')

    response = client.get(f'/api/portfolio/{portfolio_item.id}/')
    assert response.status_code == 200
    assert response.data['title'] == 'Test Portfolio Item'


@pytest.mark.django_db(transaction=True)
@pytest.fixture(scope='function', autouse=True)
def clean_up_database(transactional_db):
    pass