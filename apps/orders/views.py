from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.catalog.permissions import IsOwnerOrReadOnly
from .models import Order
from .serializers import (
    OrderReadSerializer, 
    OrderWriteSerializer, 
    OrderCheckSerializer, 
    get_cart_items, 
    calculate_total, 
    OrderUpdateSerializer
)


class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(responses={200: OrderReadSerializer(many=True)})
    def get(self, request):
        print(f"DEBUG: Request user is -> {request.user.username} (ID: {request.user.id})")
        orders = Order.objects.filter(user=request.user).prefetch_related('order_items__product')
        serializer = OrderReadSerializer(orders, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=OrderWriteSerializer,
        responses={201: OrderReadSerializer}
    )
    def post(self, request):
        serializer = OrderWriteSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        return Response(OrderReadSerializer(order).data, status=status.HTTP_201_CREATED)



class OrderDetailUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    @extend_schema(responses={200: OrderReadSerializer})
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, order)
        serializer = OrderReadSerializer(order)
        return Response(serializer.data)

    @extend_schema(
        request=OrderUpdateSerializer,
        responses={200: OrderReadSerializer}
    )
    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, order)
        
        
        serializer = OrderUpdateSerializer(order, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(OrderReadSerializer(order).data)



class OrderCheckView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=OrderCheckSerializer, responses={200: OrderCheckSerializer})
    def post(self, request):
        serializer = OrderCheckSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        items = serializer.validated_data['items']
        cart_items = get_cart_items(request.user, items)
        total = calculate_total(cart_items, serializer.validated_data['payment_method'])

        return Response({"ok": True, "total": total})


