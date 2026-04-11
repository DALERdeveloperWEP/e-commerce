from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.catalog.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly
from .models import Order, OrderItem
from .serializers import OrderSerializer
from ..cart.models import CartItem


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsUserOrReadOnly, IsOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Response(self.queryset.filter(user=self.request.user))
