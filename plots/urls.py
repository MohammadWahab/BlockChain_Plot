# plots/urls.py
from django.urls import path
from .views import (
    CustomUserListView,
    CustomUserDetailView,
    PlotListView,
    PlotDetailView,
    TransferPlotOwnershipView,
)

urlpatterns = [
    path('users/', CustomUserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),

    path('plots/', PlotListView.as_view(), name='plot-list'),
    path('plots/<int:pk>/', PlotDetailView.as_view(), name='plot-detail'),

    path('transfer_plot_ownership/<int:pk>/', TransferPlotOwnershipView.as_view(), name='transfer-ownership'),
    
]
