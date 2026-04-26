from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.utils.text import slugify

from .models import Category, Product, Favorite 
from ..seller.models import CategoryRequest



class UniversalCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = serializers.ImageField()
    slug = serializers.SlugField()
    created_by_type = serializers.SerializerMethodField()
    
    def get_created_by_type(self, obj):
        if isinstance(obj, CategoryRequest):
            return "seller"
        return "admin"


class CategoryUpdateSerializser(serializers.Serializer):
    name = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    slug = serializers.SlugField(read_only=False)
    created_by_type = serializers.ChoiceField(choices=['admin', 'seller'])


class CategoryDeleteSerializser(serializers.Serializer):
    created_by_type = serializers.ChoiceField(choices=['admin', 'seller'], write_only=True)


class CategorySerailzer(ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'slug']
        read_only_fields = ['id', 'slug']
        
    
    def update(self, instance, validated_data):
        match validated_data['created_by_type']:
            case 'seller':
                get_category_request = CategoryRequest.objects.filter(id=validated_data.get('id', None)).first()
                for attr, value in validated_data.items():
                    setattr(get_category_request, attr, value)
                get_category_request.save()
                return get_category_request
            case 'admin':
                return super().update(instance, validated_data)
            case _:
                raise serializers.ValidationError({
                    "created_by_type": "created_by_type must be either 'admin' or 'seller'"
                })
                
    
        
        


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