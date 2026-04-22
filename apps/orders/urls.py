from django.urls import path
from .views import OrderDetailUpdateView, OrderListCreateView, OrderCheckView

urlpatterns = [
    path('', OrderListCreateView.as_view()),
    path('<int:pk>/', OrderDetailUpdateView.as_view()),
    path('check/', OrderCheckView.as_view()),
]
