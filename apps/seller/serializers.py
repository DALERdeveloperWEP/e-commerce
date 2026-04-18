from django.utils.text import slugify
from rest_framework import serializers

from ..catalog.models import Category
from .models import CategoryRequest

class SellerCategoriesSerializer(serializers.Serializer):
    class Meta:
        model = CategoryRequest
        fields = ['id', 'name', 'image', 'slug', 'status']
        read_only_fields = ['id', 'slug']
    
    def validate(self, attrs):
        if attrs.get('name'):
            if not Category.objects.filter(name=attrs.get('name')).exists():
                raise serializers.ValidationError({"name": "A category with this name already exists."})
        
        if not self.context['request'].user.is_seller:
            raise serializers.ValidationError({"detail": "Only sellers can create category requests."})
        
        return super().validate(attrs)
    
    
    def save(self, **kwargs):
        base_slug = slugify(self.title)
        slug = base_slug
        
        counter = 1
        
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter+=1
            
        self.slug = slug 
        return super().save(**kwargs)
    

class CategoryRequestCancelSerializer(serializers.Serializer):
    class Meta:
        model = CategoryRequest
        fields = ['id', 'name', 'image', 'slug', 'status']
        read_only_fields = ['id', 'slug', 'image', 'name']
        
    def validate(self, attrs):
        if attrs.get('status') != 'cancel':
            raise serializers.ValidationError({"status": "Status must be 'cancel'."})
        return super().validate(attrs)
    