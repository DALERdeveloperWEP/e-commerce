from rest_framework import serializers
from decouple import config

from .models import Order, OrderItem
from ..cart.models import CartItem
from ..catalog.serializers import ProductSerailzer



def get_cart_items(user, ids):
    return CartItem.objects.filter(
        id__in=ids,
        cart__user=user
    ).select_related('product')


def calculate_total(cart_items):
    return sum(i.product.price * i.quantity for i in cart_items)


class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerailzer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(source='order_items', many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'full_name', 'phone', 'address', 'house', 
            'apartment', 'comment', 'total_price', 'status', 'items'
        ]


class OrderWriteSerializer(serializers.ModelSerializer):
    
    input_items = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True,
        required=False
    )

    class Meta:
        model = Order
        fields = [
            'full_name', 'phone', 'address', 'house', 
            'apartment', 'comment', 'status', 'input_items'
        ]
        read_only_fields = ['status']

    def validate(self, attrs):
        
        if self.context['request'].method == 'POST' and 'input_items' not in attrs:
            raise serializers.ValidationError({"input_items": "Bu maydon bo'lishi shart."})
        return attrs

    def create(self, validated_data):
        item_ids = validated_data.pop('input_items')
        user = self.context['request'].user
        
        cart_items = get_cart_items(user, item_ids)
        if cart_items.count() != len(set(item_ids)):
            raise serializers.ValidationError("Ba'zi mahsulotlar savatchada topilmadi.")

        total = calculate_total(cart_items)
        if total < config('MIN_PRICE', cast=int):
            raise serializers.ValidationError(f"Minimal summa: {config('MIN_PRICE')}р")

        order = Order.objects.create(user=user, total_price=total, **validated_data)
        
        order_items = [
            OrderItem(order=order, product=i.product, quantity=i.quantity, price=i.product.price)
            for i in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)
        cart_items.delete()
        return order

   


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'full_name', 'phone', 'address', 'house', 
            'apartment', 'comment', 'status'
        ]



class OrderCheckSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.IntegerField()
    )
    
    def validate_items(self, value):
        
        cart_items = get_cart_items(self.context['request'].user, value)

        if set(cart_items.values_list('id', flat=True)) != set(value):
            raise serializers.ValidationError("Ba'zi CartItem lar topilmadi")

        min_price = config("MIN_PRICE", cast=int)

        total = calculate_total(cart_items)
        

        if  total < min_price:
            raise serializers.ValidationError({
                "total_price": f"Минимальная сумма заказа {min_price}р"
            })

        return value
    
