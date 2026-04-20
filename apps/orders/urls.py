from django.urls import path
from .views import OrderDetailUpdateView, OrderListCreateView, OrderCheckView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view()),
    path('orders/<int:pk>', OrderDetailUpdateView.as_view()),
    path('check/', OrderCheckView.as_view()),
]
