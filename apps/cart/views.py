from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import CartItem, Cart
from .serializers import CartItemSerializer
from ..catalog.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly


class CartItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsUserOrReadOnly, IsOwnerOrReadOnly]
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
        return Response(serializer.data, status=status.HTTP_200_OK)
        