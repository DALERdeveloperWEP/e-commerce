from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Category, Product, Favorite 



class CategorySerailzer(ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'slug']
        read_only_fields = ['id', 'slug']
        


class ProductSerailzer(ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Product
        fields = '__all__'
    
    def validate(self, attrs):
        regular_price = attrs.get('regular_price')
        card_price = attrs.get('card_price')
        discount_percent = attrs.get('discount_percent')
        
        if discount_percent is not None:
            if discount_percent < 0 or discount_percent > 100:
                raise serializers.ValidationError({
                    "discount_percent": "0 dan 100 gacha bo‘lishi kerak"
                })

        if card_price is not None and regular_price is not None:
            if card_price > regular_price:
                raise serializers.ValidationError({
                    "card_price": "Card price regular price dan katta bo‘lishi mumkin emas"
                })
            
        return super().validate(attrs)
    


class FavoritSerailzer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['product']
        read_only_fields = ['user']