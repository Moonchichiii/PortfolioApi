from django.urls import path
from .views import PortfolioItemListCreateView, PortfolioItemDetailView

urlpatterns = [
    path('portfolio/', PortfolioItemListCreateView.as_view(), name='portfolio-list-create'),
    path('portfolio/<int:pk>/', PortfolioItemDetailView.as_view(), name='portfolio-detail'),
]
