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


def calculate_total(cart_items, payment_method):
    match payment_method:
        case 'regular_price':
            return sum(i.product.regular_price * i.quantity for i in cart_items)
        case 'card_price':
            return sum(i.product.card_price * i.quantity for i in cart_items)
        case _:
            return sum(i.product.regular_price * i.quantity for i in cart_items)


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
    payment_method = serializers.ChoiceField(
        choices=['regular_price', 'card_price'], 
        write_only=True, 
        required=False,
        default='regular_price'
    )

    class Meta:
        model = Order
        fields = [
            'full_name', 'phone', 'address', 'house', 'apartment', 
            'comment', 'status', 'input_items', 'payment_method'
        ]
        read_only_fields = ['status']

    def validate(self, attrs):
        
        if self.context['request'].method == 'POST' and 'input_items' not in attrs:
            raise serializers.ValidationError({"input_items": "Bu maydon bo'lishi shart."})
        return attrs

    def create(self, validated_data):
        item_ids = validated_data.pop('input_items')
        user = self.context['request'].user
        payment_method = validated_data.pop('payment_method', 'regular_price')
        
        cart_items = get_cart_items(user, item_ids)
        if cart_items.count() != len(set(item_ids)):
            raise serializers.ValidationError("Ba'zi mahsulotlar savatchada topilmadi.")

        total = calculate_total(cart_items, payment_method)
        if total < config('MIN_PRICE', cast=int):
            raise serializers.ValidationError(f"Minimal summa: {config('MIN_PRICE')}р")

        order = Order.objects.create(user=user, total_price=total, **validated_data)
        
        order_items = [
            OrderItem(
                order=order, 
                product=i.product, 
                quantity=i.quantity, 
                price=i.product.card_price if payment_method == 'card_price' else i.product.regular_price
            ) for i in cart_items
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
    
    def validate_status(self, value):
        order_obj = self.instance
        new_status = value
        
        if new_status != 'cancelled':
            if order_obj.status == 'delivered':
                raise serializers.ValidationError({"status": "Yetkazib berilgan buyurtmani bekor qilib bo'lmaydi!"})
            else:
                raise serializers.ValidationError({"status": 'Buyurtma Holati Faqat Bekor qilish mumkin'})
        elif order_obj.status == 'cancelled':
            raise serializers.ValidationError({"status": "Buyurtma Bekor qilin gandan keyin uni holatini ozgar tirib bolmaydi"})
        
        return value



class OrderCheckSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.IntegerField()
    )
    payment_method = serializers.ChoiceField(
        choices=['regular_price', 'card_price'], 
        write_only=True, 
        required=False,
        default='regular_price'
    )
    
    
    def validate(self, attrs): 
        items_ids = attrs.get('items')
        payment_method = attrs.get('payment_method', 'regular_price')
        
        cart_items = get_cart_items(self.context['request'].user, items_ids)
        if cart_items.count() != len(set(items_ids)):
            raise serializers.ValidationError({"items": "Ba'zi CartItem lar topilmadi"})

        total = calculate_total(cart_items, payment_method)
        min_price = config("MIN_PRICE", cast=int)

        if total < min_price:
            raise serializers.ValidationError({
                "total_price": f"Минимальная сумма заказа {min_price}р",
                "current_total": total
            })
            
        

        attrs['total'] = total 
        return attrs
    
