from django.utils.text import slugify
from rest_framework import serializers
from ..catalog.models import Category
from .models import CategoryRequest

class SellerCategoriesSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    status = serializers.CharField(required=False) 

    class Meta:
        model = CategoryRequest
        fields = ['id', 'name', 'image', 'slug', 'status', 'comment']
        read_only_fields = ['id', 'slug']

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user if request else None

        if user and not getattr(user, 'is_seller', False):
            raise serializers.ValidationError({"detail": "Only sellers can perform this action."})


        name = attrs.get('name')
        if name:
            if Category.objects.filter(name=name).exists():
                raise serializers.ValidationError({"name": "A category with this name already exists."})


        if 'status' in attrs and attrs.get('status') != 'cancel':
            raise serializers.ValidationError({"status": "Status must be 'cancel'."})

        return attrs

    def create(self, validated_data):

        name = validated_data.get('name')
        validated_data['slug'] = self._generate_unique_slug(name)
        return super().create(validated_data)

    def update(self, instance, validated_data):

        name = validated_data.get('name')
        
        user = self.context['request'].user
        
        if name:
            instance.slug = self._generate_unique_slug(name)
        
        match validated_data.get('status', None):
            case 'pending':
                pass
            case 'cancel':
                instance.status = 'cancel'
                
            case 'completed':
                if self.context['request'].user.is_admin:
                    instance.status = 'completed'
                
        return super().update(instance, validated_data)

    def _generate_unique_slug(self, name):
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug