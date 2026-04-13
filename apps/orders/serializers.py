from rest_framework import serializers
from decouple import config

from .models import Order, OrderItem
from ..cart.models import CartItem

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    class Meta:
        model = Order
        fields = [
            'full_name', 
            'phone', 
            'address', 
            'house', 
            'apartment', 
            'comment', 
            'total_price', 
            'status',
            'items',
        ]
        read_only_fields = ['status', 'total_price']

    
    def validate_items(self, value):
        
        for item_id in value:
            if not CartItem.objects.filter(id=item_id).exists():
                raise serializers.ValidationError(f"CartItem with id {item_id} does not exist.")
        

        min_price = config("MIN_PRICE", cast=int)
        
        total = 0

        for item in value:
            total += item.product.price * item.quantity

        if total < min_price:
            raise serializers.ValidationError({
                "total_price": f"Минимальная сумма заказа {min_price}р"
            })
            
        return value
    
    def create(self, validated_data):
        items = validated_data.pop("items")
        user = self.context['request'].user

        order = Order.objects.create(user=user, **validated_data)

        total = 0

        cart_items = CartItem.objects.filter(id__in=items)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            total += item.product.price * item.quantity
        
        order.total_price = total
        order.save()

        return order
    



class OrderCheckSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.IntegerField()
    )
    
    def validate_items(self, value):
        
        for item_id in value:
            if not CartItem.objects.filter(id=item_id).exists():
                raise serializers.ValidationError(f"CartItem with id {item_id} does not exist.")
        

        min_price = config("MIN_PRICE", cast=int)
        
        total = 0

        for item in value:
            total += item.product.price * item.quantity

        if total < min_price:
            raise serializers.ValidationError({
                "total_price": f"Минимальная сумма заказа {min_price}р"
            })
            
        return value