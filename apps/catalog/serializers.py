from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.utils.text import slugify

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
        read_only_fields = ['slug']
    
    def validate(self, attrs):
        regular_price = attrs.get('regular_price')
        card_price = attrs.get('card_price')
        discount_percent = attrs.get('discount_percent')
        title = attrs.get('title')
        
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
        
        # if title is not None and Product.objects.filter(title=title).exists():
        #     raise serializers.ValidationError({"title": f"{title} - Bunday nomli mahsulot mavjud"})
            
        return super().validate(attrs)
    

    def save(self, **kwargs):
        
        base_slug = slugify(self.title)
        slug = base_slug
        
        counter = 1
        
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter+=1
            
        self.slug = slug 
        
        return super().save(**kwargs)
    


class FavoritSerailzer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'product']
        read_only_fields = ['user']