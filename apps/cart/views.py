from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from .models import CartItem, Cart
from .serializers import CartItemSerializer
from ..catalog.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly


class CartItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    
    
    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        product_id = request.data.get("product")

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increase(self, request, pk=None):
        item = self.get_object()
        item.quantity += 1
        item.save()
        return Response(self.get_serializer(item).data)

    @action(detail=True, methods=['post'])
    def decrease(self, request, pk=None):
        item = self.get_object()

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.get_serializer(item).data)
        