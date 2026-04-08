from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import CartItem
from .serializers import CartItemSerializer


class CartItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    
    def perform_create(self, serializer):
        
    
    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)