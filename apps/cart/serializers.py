from .models import CartItem
from rest_framework import serializers

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']
        read_only_fields = ['id', 'quantity']