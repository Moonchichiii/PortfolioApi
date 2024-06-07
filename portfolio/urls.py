from django.urls import path
from .views import PortfolioItemListCreateView, PortfolioItemDetailView

urlpatterns = [
    path('', PortfolioItemListCreateView.as_view(), name='portfolio-list-create'),
    path('<int:pk>/', PortfolioItemDetailView.as_view(), name='portfolio-detail'),
]
