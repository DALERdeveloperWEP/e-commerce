from django.urls import path

from .views import CategoryRequestListCreateView, CategoryRequestDetailView

urlpatterns = [
    path('category/requests/', CategoryRequestListCreateView.as_view()),
    path('category/requests/<int:pk>', CategoryRequestDetailView.as_view()),
    # path('products/'),
]
