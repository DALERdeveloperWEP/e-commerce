from django.urls import path
from .views import (
    AdminDashboardView,
    SellerDashboardView,
    AdminProductsView,
    SellerProductsView,
    AdminOrdersView,
    SellerOrdersView,
    AdminCategoriesView,
    SellerCategoriesView,
    AdminStatisticsView,
    SellerStatisticsView,
    AdminAdminToolsView,
    NotificationsView,
)

urlpatterns = [
    path('dashboard/admin/', AdminDashboardView.as_view()),
    path('products/admin/', AdminProductsView.as_view()),
    path('orders/admin/', AdminOrdersView.as_view()),
    path('categories/admin/', AdminCategoriesView.as_view()),
    path('statistics/admin/', AdminStatisticsView.as_view()),
    
    path('dashboard/seller/', SellerDashboardView.as_view()),
    path('products/seller/', SellerProductsView.as_view()),
    path('orders/seller/', SellerOrdersView.as_view()),
    path('categories/seller/', SellerCategoriesView.as_view()),
    path('statistics/seller/', SellerStatisticsView.as_view()),
    
    path('admin-tools/', AdminAdminToolsView.as_view()),
    path('notifications/', NotificationsView.as_view()),
]
