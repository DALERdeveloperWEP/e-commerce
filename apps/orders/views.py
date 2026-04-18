from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from drf_spectacular.utils import extend_schema

from decouple import config

from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.catalog.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly
from .models import Order
from .serializers import OrderSerializer, OrderCheckSerializer
from ..cart.models import CartItem


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsUserOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Response(self.queryset.filter(user=self.request.user))
    
    @extend_schema(
        request=OrderCheckSerializer,
        responses={200: OrderCheckSerializer}
    )
    @action(detail=False, methods=['post'])
    def check(self, request):
        serializer = OrderCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        items = serializer.validated_data['items']

        cart_items = CartItem.objects.filter(
            id__in=items,
            cart__user=request.user
        )

        if not cart_items.exists():
            return Response({
                "error": "Cart bo‘sh"
            }, status=400)

        total = sum(item.product.price * item.quantity for item in cart_items)

        if total < config('MIN_PRICE', cast=int):
            return Response({
                "error": f"Минимальная сумма заказа {config('MIN_PRICE', cast=int)}р",
                "total": total
            }, status=400)

        return Response({
            "ok": True,
            "total": total
        })
